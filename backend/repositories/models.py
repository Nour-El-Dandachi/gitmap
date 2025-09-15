from django.db import models
from users.models import User

class Repository(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=500)
    branch = models.CharField(max_length=100, default='main')
    default_branch = models.CharField(max_length=100, default='main')
    is_watched = models.BooleanField(default=True)
    is_indexed = models.BooleanField(default=False)
    index_status = models.CharField(max_length=50, default='pending')
    metadata = models.JSONField(null=True, blank=True)
    has_map = models.BooleanField(default=False)
    pinned_by = models.ManyToManyField(User, related_name="pinned_repositories", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RepoFile(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    parent_path = models.CharField(max_length=1000, null=True, blank=True)
    extension = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=50)
    sha = models.CharField(max_length=100)
    size = models.PositiveIntegerField(null=True, blank=True)
    is_binary = models.BooleanField(default=False)
    is_indexed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FileContent(models.Model):
    id = models.AutoField(primary_key=True)
    repo_file = models.ForeignKey(RepoFile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class FileChunk(models.Model):
    id = models.AutoField(primary_key=True)
    repo_file = models.ForeignKey(RepoFile, on_delete=models.CASCADE)
    chunk_index = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ChunkEmbedding(models.Model):
    id = models.AutoField(primary_key=True)
    chunk = models.OneToOneField(FileChunk, on_delete=models.CASCADE)
    embedding = models.JSONField() # or models.BinaryField()
    model_used = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)