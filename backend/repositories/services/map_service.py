#repositories/services/map_service.py

import re
from repositories.models import RepoFile, FileContent

IMPORT_LINE_REGEX = re.compile(r'^\s*(import|from|require|include|use|#include)\b.*$', re.IGNORECASE | re.MULTILINE)

def extract_import_lines_for_repo(repo_id):
    file_contents = FileContent.objects.filter(
        repo_file__repository_id=repo_id
    ).select_related("repo_file")

    result = {}

    for file_content in file_contents:
        file_path = file_content.repo_file.path
        content = file_content.content

        import_lines = re.findall(IMPORT_LINE_REGEX, content)
        all_lines = content.splitlines()
        matching_lines = [line for line in all_lines if re.match(IMPORT_LINE_REGEX, line)]

        result[file_path] = matching_lines

        print(f"[DEBUG] {file_path} imports:")
        for line in import_lines:
            print("  >>", line)


    return result


def resolve_import_links(repo_id, import_map):
    repo_files = RepoFile.objects.filter(repository_id=repo_id)
    file_paths = [f.path for f in repo_files]

    resolved_links = {}

    for source_file, import_lines in import_map.items():
        resolved_targets = []

        for line in import_lines:
            original_line = line
            line_clean = (
                line.lower()
                .replace(";", "")
                .replace("\\", "/")
                .replace("//", "/")
                .replace("'", "")
                .replace('"', "")
                .replace("use ", "")
                .replace("import ", "")
                .replace("from ", "")
                .strip()
            )

            guess_parts = line_clean.split("/")
            
            if guess_parts:
                last_guess = guess_parts[-1].split(".")[0]
                guess_parts.append(last_guess)

            for file_path in file_paths:
                path_clean = file_path.lower()

                
                if source_file == file_path:
                    continue

                filename = file_path.split("/")[-1].split(".")[0]

                if any(part in path_clean for part in guess_parts) or filename in line_clean:
                    print(f"MATCH FOUND: '{original_line}' → {file_path}")
                    resolved_targets.append(file_path)
                    break

        if resolved_targets:
            resolved_links[source_file] = resolved_targets

    return resolved_links
