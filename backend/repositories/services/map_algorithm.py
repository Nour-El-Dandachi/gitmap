#/services/map_algorithm.py

from repositories.models import RepoFile

ALLOWED_EXTENSIONS = [".php", ".py", ".js", ".ts", ".tsx", ".jsx", ".java"]


EXCLUDED_DIR_KEYWORDS = [
    "migrations", "tests", "seeders", "factories",
    "views", "templates", "config", "assets", "storage", "static"
]

def get_mappable_files(repo_id: int):
    """Return only meaningful code files for map building"""
    qs = RepoFile.objects.filter(
        repository_id=repo_id,
        is_indexed=True,
        is_binary=False
    ).only("id", "file_name", "path", "extension")

    result = []

    for file in qs:
        ext = (file.extension or "").lower()
        if ext not in ALLOWED_EXTENSIONS:
            continue

        # Exclude based on directory keywords
        path = file.path.lower()
        if any(excluded in path for excluded in EXCLUDED_DIR_KEYWORDS):
            continue

        result.append({
            "id": file.id,
            "file": file.file_name,
            "path": file.path,
        })

    return result

from repositories.models import FileContent, RepoFile
from .map_service import (
    parse_php_imports,
    parse_python_imports,
    parse_js_imports,
    parse_java_imports
)

def build_file_dependencies(repo_id: int):
    mappable_files = get_mappable_files(repo_id)
    path_to_file = {file["path"]: file for file in mappable_files}
    file_ids = [file["id"] for file in mappable_files]

    file_contents = FileContent.objects.filter(
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


from repositories.models import RepoFile

def resolve_import_path(import_str: str, all_paths: set[str]) -> str | None:
    """
    Tries to match an import string like 'app.models.User' to an actual file path.
    """
    candidates = []

    
    path_style = import_str.replace(".", "/")

    
    for ext in [".php", ".py", ".js", ".ts", ".java"]:
        candidates.append(f"{path_style}{ext}")
        candidates.append(f"{path_style.lower()}{ext}")

    for candidate in candidates:
        if candidate in all_paths:
            return candidate
    return None


def build_file_edges(repo_id: int, parsed_files: list[dict]) -> list[dict]:
    """
    Creates edges based on the parsed imports and existing RepoFile paths.
    """
    files_by_path = RepoFile.objects.filter(repository_id=repo_id, is_indexed=True)
    available_paths = set(f.path for f in files_by_path)

    edges = []

    for file in parsed_files:
        source_path = file["path"]
        imports = file.get("imports", [])

        for imp in imports:
            target_path = resolve_import_path(imp, available_paths)
            if target_path:
                edges.append({
                    "source": source_path,
                    "target": target_path
                })

    return edges

from repositories.services.map_algorithm import (
    build_file_dependencies,
    build_file_edges
)


def build_code_map(repo_id: int) -> dict:
    parsed_files = build_file_dependencies(repo_id)
    edges = build_file_edges(repo_id, parsed_files)

    nodes = [
        {"id": f["path"], "label": f["file"]}
        for f in parsed_files
    ]

    return {"nodes": nodes, "edges": edges}
