from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    github_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    github_login = models.CharField(max_length=255, null=True, blank=True)
    github_token = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username or self.email
