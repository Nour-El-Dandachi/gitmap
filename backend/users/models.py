from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    github_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    github_login = models.CharField(max_length=255, null=True, blank=True)
    github_token = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('user', 'user'), ('admin', 'admin')], default='user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email or "User"
