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

