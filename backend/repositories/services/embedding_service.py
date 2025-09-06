#/services/embedding_service.py
import os
from repositories.models import RepoFile



class EmbeddingService:

    @staticmethod
    def embed_repository(repo, embed_fn):
        from repositories.services.repo_service import RepoService

        indexed_files = RepoFile.objects.filter(repository=repo, is_indexed=True)

        for file in indexed_files:
            try:
                result = RepoService.fetch_file_content(repo.owner, repo.name, file.sha)
                content = result.get("content", "")

                if not content.strip():
                    continue

                embedding = embed_fn(content)

                print(f"[{file.path}] -> {embedding[:5]}...") 

                # TODO: Save to DB or vector store
                # Example: file.embedding = embedding; file.save()

            except Exception as e:
                print(f"Failed to embed {file.path}: {e}")