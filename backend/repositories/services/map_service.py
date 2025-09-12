# repositories/services/map_service.py
import re
import ast
import os
import json
import anthropic
from repositories.models import FileContent, RepoFile

# Initialize Claude client with key from .env
claude_client = anthropic.Anthropic(api_key=os.environ.get("CLAUDE_KEY"))

def parse_php_imports(content: str) -> list[str]:
    imports = set()

    content = re.sub(r'//.*?$|/\*.*?\*/', '', content, flags=re.DOTALL | re.MULTILINE)

    use_pattern = re.compile(r'^\s*use\s+([A-Za-z0-9_\\]+);', re.MULTILINE)
    imports.update(use_pattern.findall(content))

    include_pattern = re.compile(r'^\s*(?:include|require)(_once)?\s*[\'"]([^\'"]+)[\'"];', re.MULTILINE)
    imports.update([match[1] for match in include_pattern.findall(content)])

    fqcn_pattern = re.compile(r'new\s+\\([A-Za-z0-9_\\]+)')
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
    pattern = re.compile(
        r"""
        import\s+[^'"]*?['"]([^'"]+)['"]  |   
        require\(['"]([^'"]+)['"]\)       |   
        import\(['"]([^'"]+)['"]\)            
        """,
        re.VERBOSE
    )
    matches = pattern.findall(content)
    imports = [m for group in matches for m in group if m]
    return list(set(imports))


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
        path = fc.repo_file.path
        ext = (fc.repo_file.extension or "").lower()
        content = fc.content

        imports = []
        if ext == ".php":
            imports = parse_php_imports(content)
        elif ext == ".py":
            imports = parse_python_imports(content)
        elif ext in [".js", ".jsx", ".ts", ".tsx"]:
            imports = parse_js_imports(content)
        elif ext == ".java":
            imports = parse_java_imports(content)

        results.append({
            "file": fc.repo_file.file_name,
            "path": path,
            "imports": imports
        })

        print(f"[DEBUG] {path} → {imports}")

    return results


def list_indexed_files_for_llm(repo_id: int):
    qs = RepoFile.objects.filter(repository_id=repo_id, is_indexed=True).only("id", "file_name", "path")
    out = []
    for f in qs:
        fname = f.file_name
        out.append({"id": f.id, "file": fname, "path": f.path})
    return out


def get_key_files_for_map(repo_id: int):
    files = list_indexed_files_for_llm(repo_id)

    prompt = f"""
You are a codebase analysis assistant.

You are given a list of files from a repository. Each file has an id, name, and path.

Your task:
- Select only the most important files needed to understand how the codebase works and how files are connected.
- Exclude any files that are:
  - Migrations
  - Seeds
  - Configs
  - Factories
  - Views/templates
  - Assets (CSS, JS, images)
  - Tests
  - Routes
- Return a clean JSON array of file objects. Each must include:
  - id
  - file
  - path

Respond ONLY with the valid JSON. No markdown. No explanation.

Here is the input:

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
            content = content.strip("```json").strip("```")
        result = json.loads(content)
        return result
    except Exception as e:
        print("[AI PARSE ERROR]", e)
        return {
            "error": "Invalid JSON from AI",
            "raw": content
        }


def generate_connections_from_imports(parsed_imports: list[dict]):
    prompt = f"""
You are given the following repository structure with files and their imports:

{json.dumps(parsed_imports, indent=2)}

Output a **valid raw JSON** object with this structure:
{{
  "nodes": [{{"id": "file_path", "label": "file_name"}}],
  "edges": [{{"source": "file_path", "target": "file_path"}}]
}}

Rules:
- Use "source" and "target" (not "from"/"to")
- Ignore external libraries like Illuminate, Symfony, etc.
- **Imports**: If file A imports/uses file B, add {{"source": "A", "target": "B"}}.
- **Inheritance**: If `class X extends Y`, add edge from X → Y.
- Do NOT explain anything. No markdown. Just valid JSON.
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
            content = content.strip("```json").strip("```")
        result = json.loads(content)
        return result
    except Exception as e:
        print("[AI PARSE ERROR - CONNECTION MAP]", e)
        return {
            "error": "Invalid JSON from AI",
            "raw": content
        }


def get_codebase_map(repo_id: int):
    important_files = get_key_files_for_map(repo_id)

    if "error" in important_files:
        return important_files

    file_ids = [f["id"] for f in important_files]
    parsed = build_file_imports(repo_id, file_ids)

    result = generate_connections_from_imports(parsed)
    return result
