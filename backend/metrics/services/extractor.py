import os
import subprocess
import tempfile
import json
import shutil

from lizard import analyze_file

from metrics.models import FileMetrics
from repositories.models import RepoFile, FileContent


def extract_metrics_for_file(repo_file: RepoFile):

    file_content = FileContent.objects.filter(repo_file=repo_file).last()
    if not file_content:
        print(f"No content found for {repo_file.path}")
        return {}

    ext = repo_file.extension
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(file_content.content.encode("utf-8"))
        tmp_path = tmp.name

    metrics = {}

    CLOC_PATH = shutil.which("cloc") or "cloc"

    try:
        cloc_output = subprocess.check_output(
            [CLOC_PATH, "--json", tmp_path],
            universal_newlines=True
        )
        cloc_data = json.loads(cloc_output)
        lang = next((k for k in cloc_data.keys() if k not in ["header", "SUM"]), None)
        if lang:
            metrics["iocode"] = cloc_data[lang].get("code", 0)
            metrics["iocomment"] = cloc_data[lang].get("comment", 0)
            metrics["ioblank"] = cloc_data[lang].get("blank", 0)
            metrics["iocode_and_comment"] = metrics["iocode"] + metrics["iocomment"]
            metrics["loc"] = metrics["iocode"]
    except Exception as e:
        print(f"cloc failed for {repo_file.path}:", e)

    try:
        analysis = analyze_file(tmp_path)
        functions = analysis.function_list
        if functions:
            complexities = [f.cyclomatic_complexity for f in functions]
            metrics["vg"] = max(complexities)
            metrics["evg"] = sum(complexities) / len(complexities)
            metrics["ivg"] = sum(complexities)
            metrics["branch_count"] = sum(max(c - 1, 0) for c in complexities)
        else:
            metrics["vg"] = 0
            metrics["evg"] = 0
            metrics["ivg"] = 0
            metrics["branch_count"] = 0
    except Exception as e:
        print(f"lizard failed for {repo_file.path}:", e)

    
    try:
        halstead_output = subprocess.check_output(
            ["python3", "halstead.py", tmp_path],
            universal_newlines=True
        )
        halstead_data = json.loads(halstead_output)
        metrics.update(halstead_data)
    except Exception as e:
        print(f"halstead failed for {repo_file.path}:", e)

    
    FileMetrics.objects.update_or_create(
        repo_file=repo_file,
        defaults=metrics
    )

    os.remove(tmp_path)

    return metrics
