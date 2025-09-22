# repositories/tasks.py

from celery import shared_task
from repositories.models import Repository
from repositories.services.embedding_service import EmbeddingService
from sentence_transformers import SentenceTransformer
import os

_model = None

def get_model():
    global _model
    if _model is None:
        if os.environ.get("CI"):
            return None
        _model = SentenceTransformer("/app/bge-m3")
    return _model

def embed_local(text):
    model = get_model()
    if model is None:
        raise RuntimeError("Model not available in CI environment")
    return model.encode(text).tolist()

@shared_task
def embed_repository_task(repo_id):
    try:
        repo = Repository.objects.get(id=repo_id)
        embedder = get_model()
        if embedder is None:
            print("Skipping embedding in CI environment.")
            return
        EmbeddingService.embed_repository(repo, embed_local)
        repo.index_status = "embedded"
        repo.save()
    except Repository.DoesNotExist:
        print(f"Repository with ID {repo_id} not found.")
    except Exception as e:
        print(f"Embedding task failed: {e}")
