import re
import ast
import os
import json
import anthropic
from repositories.models import FileContent, RepoFile, Repository

claude_client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_KEY"))

def parse_php_imports(content: str) -> list[str]:
    imports = set()
    content = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.DOTALL | re.MULTILINE)

    use_pattern = re.compile(r'^\s*use\s+([A-Za-z0-9_\\]+);', re.MULTILINE)
    include_pattern = re.compile(r'^\s*(?:include|require)(_once)?\s*[\'"]([^\'"]+)[\'"];', re.MULTILINE)
    fqcn_pattern = re.compile(r'new\s+\\([A-Za-z0-9_\\]+)')

    imports.update(use_pattern.findall(content))
    imports.update([m[1] for m in include_pattern.findall(content)])
    imports.update(fqcn_pattern.findall(content))

    return list(imports)


def parse_python_imports(content: str) -> list[str]:
    imports = set()
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                base = "." * node.level + (node.module or "")
                for alias in node.names:
                    imports.add(f"{base}.{alias.name}".strip("."))
    except Exception as e:
        print("[PYTHON PARSER ERROR]", e)
    return list(imports)


def parse_js_imports(content: str) -> list[str]:
    pattern = re.compile(r"""
        import\s+[^'"]*?['"]([^'"]+)['"]  |   
        require\(['"]([^'"]+)['"]\)       |   
        import\(['"]([^'"]+)['"]\)            
        """, re.VERBOSE)
    matches = pattern.findall(content)
    return list(set([m for group in matches for m in group if m]))


def parse_java_imports(content: str) -> list[str]:
    pattern = re.compile(r'^\s*import\s+(?:static\s+)?([a-zA-Z0-9_.]+);', re.MULTILINE)
    return list(set(pattern.findall(content)))


def build_file_imports(repo_id: int, file_ids: list[int]):
    file_contents = FileContent.objects.filter(
        repo_file__repository_id=repo_id,
        repo_file_id__in=file_ids
    ).select_related("repo_file")

    results = []

    for fc in file_contents:
        ext = (fc.repo_file.extension or "").lower()
        content = fc.content

        if ext == ".php":
            imports = parse_php_imports(content)
        elif ext == ".py":
            imports = parse_python_imports(content)
        elif ext in [".js", ".jsx", ".ts", ".tsx"]:
            imports = parse_js_imports(content)
        elif ext == ".java":
            imports = parse_java_imports(content)
        else:
            imports = []

        results.append({
            "id": fc.repo_file.id,
            "file": fc.repo_file.file_name,
            "path": fc.repo_file.path,
            "imports": imports
        })

        print(f"[DEBUG] {fc.repo_file.path} → {imports}")

    return results


def list_indexed_files_for_llm(repo_id: int):
    qs = RepoFile.objects.filter(repository_id=repo_id, is_indexed=True)
    return [{"id": f.id, "file": f.file_name, "path": f.path} for f in qs]


def get_key_files_for_map(repo_id: int):
    files = list_indexed_files_for_llm(repo_id)

    prompt = f"""
You are a Laravel expert assistant.

Given this list of indexed Laravel repo files, select only the most important files needed to understand how the system works and how files are connected.

Exclude:
- migrations
- seeds
- configs
- factories
- views/templates
- assets (CSS/JS/images)
- tests
- route definitions

Return a clean JSON list. Each object must include:
- id
- file
- path

Respond ONLY with valid JSON (no markdown, no explanation).

Input:
{json.dumps(files, indent=2)}
"""

    response = claude_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text.strip()

    try:
        if content.startswith("```"):
            content = content.strip("```").strip("json").strip()
        return json.loads(content)
    except Exception as e:
        print("[AI PARSE ERROR]", e)
        return {"error": "Invalid JSON from AI", "raw": content}


def generate_dependency_table(parsed_files: list[dict]):
    prompt = f"""
You are analyzing a Laravel repository.

You are given a list of files and the imports each one contains:

{json.dumps(parsed_files, indent=2)}

Your task is to generate a **3-column Markdown table** where:

- Column 1: the file ID (e.g., 42)
- Column 2: the file name (e.g., UserController.php)
- Column 3: a **list of file IDs** (e.g., 18, 23) that imported or used this file

Strict rules:
- Use only the provided file IDs — do NOT fabricate or invent any.
- Only include relationships between the given files.
- Ignore third-party imports (like Illuminate, Symfony, etc).
- If some connections are missing but **logically should exist** (e.g. Controller → Service → Model), include them using the correct IDs.
- Respond with **valid Markdown table only**. No explanation. No code blocks.
- Maintain accuracy: every ID in the table must match one from the input.
"""

    response = claude_client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text.strip()
    if content.startswith("```"):
        content = content.strip("```").strip("markdown").strip()

    markdown_response = content

    output_path = f"/app/dependency_table_repo.xlsx"

    markdown_table_to_excel(markdown_response, output_path)

    return {
        "markdown": content,
        "excel_path": output_path
    }



def get_codebase_dependency_table(repo_id: int):
    important_files = get_key_files_for_map(repo_id)
    if "error" in important_files:
        return important_files

    file_ids = [f["id"] for f in important_files]
    parsed = build_file_imports(repo_id, file_ids)

    Repository.objects.filter(id=repo_id).update(has_map=True)

    return generate_dependency_table(parsed)


import pandas as pd
from io import StringIO

def markdown_table_to_excel(markdown_str: str, output_path: str = "dependencies.xlsx"):
    markdown_str = markdown_str.strip()
    if markdown_str.startswith("```"):
        markdown_str = markdown_str.strip("```markdown").strip("```")

    df = pd.read_csv(StringIO(markdown_str), sep="|", skipinitialspace=True, engine='python')

    df = df.dropna(axis=1, how='all')

    df = df[~df[df.columns[0]].str.strip().str.contains("^-+$")]

    df.columns = [col.strip() for col in df.columns]
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    df.to_excel(output_path, index=False)

