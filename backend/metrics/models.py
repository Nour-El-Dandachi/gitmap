from django.db import models
from repositories.models import RepoFile 

class FileMetrics(models.Model):
    repo_file = models.OneToOneField(RepoFile, on_delete=models.CASCADE, related_name="metrics")

    loc = models.IntegerField(null=True, blank=True)
    vg = models.IntegerField(null=True, blank=True)
    evg = models.IntegerField(null=True, blank=True)
    ivg = models.IntegerField(null=True, blank=True)

    
    n = models.IntegerField(null=True, blank=True)
    uniq_op = models.IntegerField(null=True, blank=True)
    uniq_opnd = models.IntegerField(null=True, blank=True)
    total_op = models.IntegerField(null=True, blank=True)
    total_opnd = models.IntegerField(null=True, blank=True)

    
    v = models.FloatField(null=True, blank=True)
    l = models.FloatField(null=True, blank=True)
    d = models.FloatField(null=True, blank=True)
    i = models.FloatField(null=True, blank=True)
    e = models.FloatField(null=True, blank=True)
    b = models.FloatField(null=True, blank=True)
    t = models.FloatField(null=True, blank=True)

    iocode = models.IntegerField(null=True, blank=True)
    iocomment = models.IntegerField(null=True, blank=True)
    ioblank = models.IntegerField(null=True, blank=True)
    iocode_and_comment = models.IntegerField(null=True, blank=True)

    branch_count = models.IntegerField(null=True, blank=True)

    defects = models.BooleanField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Metrics for {self.repo_file.path}"
