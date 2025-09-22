from celery import shared_task
from repositories.models import RepoFile
from metrics.services.extractor import extract_metrics_for_file
from metrics.models import FileMetrics

@shared_task
def extract_metrics_for_repository(repo_id):
    files = RepoFile.objects.filter(repository_id=repo_id, is_binary=False)
    for f in files:
        try:
            extract_metrics_for_file(f)
            print(f"Metrics extracted for {f.path}")
        except Exception as e:
            print(f"Failed for {f.path}: {e}")
