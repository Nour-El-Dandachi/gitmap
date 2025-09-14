from map.models import NodePosition, FileEdge
from django.shortcuts import get_object_or_404
from django.utils import timezone
from map.models import NodePosition, FileEdge
from repositories.models import RepoFile

class MapService:

    @staticmethod
    def create_node_position(repo_file_id, x, y):
        repo_file = RepoFile.objects.get(id=repo_file_id)
        node, created = NodePosition.objects.update_or_create(
            repo_file=repo_file,
            defaults={'x': x, 'y': y}
        )
        return node

    @staticmethod
    def create_file_edge(source_id, target_id):
        source = RepoFile.objects.get(id=source_id)
        target = RepoFile.objects.get(id=target_id)
        edge = FileEdge.objects.create(source=source, target=target)
        return edge

    @staticmethod
    def get_all_node_positions():
        return NodePosition.objects.select_related('repo_file').all()
        
    @staticmethod
    def get_all_file_edges():
        return FileEdge.objects.select_related('source', 'target').all()
