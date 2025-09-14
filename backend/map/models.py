from django.db import models
from repositories.models import RepoFile, Repository

class NodePosition(models.Model):
    repo_file = models.OneToOneField(RepoFile, on_delete=models.CASCADE, related_name="node_position")
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return f"{self.repo_file.file_name} @ ({self.x}, {self.y})"


class FileEdge(models.Model):
    source = models.ForeignKey(RepoFile, on_delete=models.CASCADE, related_name="edge_sources")
    target = models.ForeignKey(RepoFile, on_delete=models.CASCADE, related_name="edge_targets")

    def __str__(self):
        return f"{self.source.file_name} → {self.target.file_name}"
