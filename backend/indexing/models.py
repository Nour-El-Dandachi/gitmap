from django.db import models
from users.models import User
from repositories.models import Repository

class IndexingJob(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'pending'), ('in_progress', 'in_progress'), ('done', 'done'), ('error', 'error')])
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)


class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)