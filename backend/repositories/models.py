from django.db import models
from users.models import User

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repositories")
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.URLField()
    branch = models.CharField(max_length=255, default="main")
    default_branch = models.CharField(max_length=255, default="main")
    is_watched = models.BooleanField(default=True)
    is_indexed = models.BooleanField(default=False)
    index_status = models.CharField(max_length=50, default="pending")
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner}/{self.name}"

class RepoFile(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="files")
    path = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    parent_path = models.CharField(max_length=1024, null=True, blank=True)
    extension = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50)
    sha = models.CharField(max_length=255)
    size = models.PositiveIntegerField(null=True, blank=True)
    is_binary = models.BooleanField(default=False)
    is_indexed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.path


class FileContent(models.Model):
    repo_file = models.OneToOneField(RepoFile, on_delete=models.CASCADE, related_name="content")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
