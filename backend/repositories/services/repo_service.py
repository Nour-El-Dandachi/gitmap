#/services/repo_service.py
import requests
from urllib.parse import urlparse
import base64
import os
import json
import openai
from django.conf import settings


from repositories.models import Repository, RepoFile
from indexing.models import IndexingJob
from django.db.models import Q
from repositories.tasks import embed_repository_task


GITHUB_API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "GitMap"
}

ACCEPTED_EXTENSIONS = [
    ".py", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".css", ".scss", ".java", ".php",
    ".rb", ".go", ".cpp", ".c", ".cs", ".json", ".yml", ".yaml", ".md"
]

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
            raise Exception(f"Failed to fetch file content: {response.status_code} - {response.text}")

        data = response.json()

        if data.get("encoding") != "base64":
            raise Exception("Blob encoding is not base64")

        if "content" not in data:
            raise Exception("Content not found in blob response")

        try:
            decoded = base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
        except Exception as e:
            raise Exception(f"Decoding failed for SHA {sha}: {str(e)}")

        return {
            "content": decoded
        }

    @staticmethod
    def start_indexing_workflow(user, url, branch):
        parsed = RepoService.parse_repo_url(url)
        owner, repo_name = parsed["owner"], parsed["repo"]

        if not owner or not repo_name:
            raise ValueError("Invalid GitHub repository URL")

        repo_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}"
        response = requests.get(repo_url, headers=HEADERS)

        if response.status_code != 200:
            raise ValueError("GitHub repository not found")

        repo_metadata = response.json()
        default_branch = repo_metadata.get("default_branch", branch)
        description = repo_metadata.get("description", "")
        stars = repo_metadata.get("stargazers_count", 0)

        repo = Repository.objects.create(
            user=user,
            owner=owner,
            name=repo_name,
            url=url,
            branch=branch,
            default_branch=default_branch,
            is_watched=True,
            is_indexed=False,
            index_status="pending",
            metadata={
                "description": description,
                "stars": stars
            }
        )

        IndexingJob.objects.create(repository=repo, status="pending")

        folders = RepoService.save_repo_tree(repo)
        repo.index_status = "tree_saved"
        repo.save()

        languages = RepoService.fetch_languages(owner, repo_name)

        important_folders = RepoService.ask_ai_for_folders(
            repo_name=repo.name,
            description=description,
            languages=languages,
            folders=folders
        )

        repo.metadata["important_folders"] = important_folders

        query = Q()
        for folder in important_folders:
            query |= Q(parent_path__startswith=folder)

        RepoFile.objects.filter(repository=repo).filter(query).update(is_indexed=True)

        repo.index_status = "folders_selected"
        repo.save()

        embed_repository_task.delay(repo.id)


        return repo

    @staticmethod
    def fetch_languages(owner, repo_name):
        lang_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/languages"
        response = requests.get(lang_url, headers=HEADERS)
        if response.status_code != 200:
            return []

        return list(response.json().keys())

    @staticmethod
    def save_repo_tree(repo: Repository):
        owner = repo.owner
        name = repo.name
        branch = repo.default_branch

        tree_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/git/trees/{branch}?recursive=1"
        response = requests.get(tree_url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception("Failed to fetch GitHub tree")

        tree = response.json().get("tree", [])
        folders = []

        for item in tree:
            if item["type"] == "tree":
                folders.append(item["path"])
            elif item["type"] == "blob":
                path = item["path"]
                sha = item["sha"]
                size = item.get("size", 0)
                file_name = os.path.basename(path)
                parent_path = os.path.dirname(path)
                extension = os.path.splitext(file_name)[1].lower()

                if extension not in ACCEPTED_EXTENSIONS or size > 200_000:
                    continue

                RepoFile.objects.create(
                    repository=repo,
                    path=path,
                    file_name=file_name,
                    parent_path=parent_path,
                    extension=extension,
                    type="code",
                    sha=sha,
                    size=size,
                    is_binary=False,
                    is_indexed=False
                )

        repo.is_indexed = False
        return folders

    @staticmethod
    def ask_ai_for_folders(repo_name, description, languages, folders):
        openai.api_key = settings.OPENAI_API_KEY

        prompt = f"""
        You are an AI system helping index GitHub repositories.

        Repo name: {repo_name}
        Description: {description}
        Languages used: {', '.join(languages)}
        Folders in repo: {folders}

        Pick the most relevant folders (max 5) that likely contain core logic (e.g. routes, services, controllers, APIs).

        Return ONLY a JSON list of folder paths. Like:
        ["src", "api", "app/services"]
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            content = response.choices[0].message.content
            print("AI raw response:", content)
            return json.loads(content)
        except json.JSONDecodeError:
            print("AI returned invalid JSON")
            return []
        except Exception as e:
            print("AI folder selection failed:", e)
            return []
