import requests
from urllib.parse import urlparse
import base64

GITHUB_API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitMap"
}

class RepoService:

    @staticmethod
    def parse_repo_url(url):
        parsed = urlparse(url)
        segments = parsed.path.strip("/").split("/")
        return {
            "owner": segments[0] if len(segments) > 0 else None,
            "repo": segments[1] if len(segments) > 1 else None
        }

    @staticmethod
    def fetch_tree(url):
        parsed = RepoService.parse_repo_url(url)
        owner, repo = parsed["owner"], parsed["repo"]

        if not owner or not repo:
            raise ValueError("Invalid GitHub repository URL")

        meta = requests.get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}")
        if meta.status_code != 200:
            raise ValueError("Repository not found")

        default_branch = meta.json().get("default_branch", "main")
        tree_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        response = requests.get(tree_url, headers=HEADERS)

        if response.status_code != 200:
            raise Exception("Failed to fetch repo tree")

        return response.json()

    @staticmethod
    def fetch_file_content(owner, repo, sha):
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/blobs/{sha}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise Exception("Failed to fetch file content")

        data = response.json()
        decoded = base64.b64decode(data["content"]).decode("utf-8")

        return {
            "filename": data.get("path", "unknown"),
            "content": decoded
        }
