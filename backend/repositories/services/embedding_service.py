# /services/embedding_service.py
import textwrap
from django.utils import timezone
from repositories.models import RepoFile, FileContent, FileChunk, ChunkEmbedding

class EmbeddingService:

    @staticmethod
    def embed_repository(repo, embed_fn):
        from repositories.services.repo_service import RepoService

        print(f"Starting embedding for repo: {repo.name}")

        indexed_files = RepoFile.objects.filter(repository=repo, is_indexed=True)

        if not indexed_files.exists():
            print(f"No indexed files found for repo: {repo.name}")
            return

        for file in indexed_files:
            try:
                print(f"Fetching content for: {file.path}")
                result = RepoService.fetch_file_content(repo.owner, repo.name, file.sha)
                content = result.get("content", "")

                if not content or not content.strip():
                    print(f"Empty content for {file.path}, skipping.")
                    continue

                file_content = FileContent.objects.create(
                    repo_file=file,
                    content=content,
                )
                print(f"Saved FileContent for {file.path}")

                chunks = textwrap.wrap(content, width=500)

                for i, chunk_text in enumerate(chunks):
                    chunk = FileChunk.objects.create(
                        repo_file=file,
                        chunk_index=i,
                        content=chunk_text,
                    )
                    print(f"Created chunk {i} for {file.path}")

                    embedding = embed_fn(chunk_text)

                    ChunkEmbedding.objects.create(
                        chunk=chunk,
                        embedding=embedding,
                        model_used="bge-m3",
                    )
                    print(f"Embedded and saved chunk {i} for {file.path}")

            except Exception as e:
                print(f"Failed to process {file.path}: {e}")
