# repositories/tasks.py

from celery import shared_task
from repositories.models import Repository
from repositories.services.embedding_service import EmbeddingService
from sentence_transformers import SentenceTransformer
import os

model = None
if not os.environ.get("CI"):
    model = SentenceTransformer("/app/bge-m3")

def embed_local(text):
    return model.encode(text).tolist()

@shared_task
def embed_repository_task(repo_id):
    try:
        repo = Repository.objects.get(id=repo_id)
        EmbeddingService.embed_repository(repo, embed_local)
        repo.index_status = "embedded"
        repo.save()
    except Repository.DoesNotExist:
        print(f"Repository with ID {repo_id} not found.")
    except Exception as e:
        print(f"Embedding task failed: {e}")
