from map.models import MapNode, MapEdge
from django.shortcuts import get_object_or_404
from django.utils import timezone

class MapService:

    @staticmethod
    def create_node(repo_file, x, y):
        return MapNode.objects.create(
            repo_file=repo_file,
            x=x,
            y=y,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

    @staticmethod
    def list_nodes_by_repo(repo_id):
        return MapNode.objects.filter(repo_file__repository_id=repo_id)

    @staticmethod
    def get_node(node_id):
        return get_object_or_404(MapNode, id=node_id)

    @staticmethod
    def update_node(node_id, x, y):
        node = MapService.get_node(node_id)
        node.x = x
        node.y = y
        node.updated_at = timezone.now()
        node.save()
        return node

    @staticmethod
    def delete_node(node_id):
        node = MapService.get_node(node_id)
        node.delete()

    @staticmethod
    def create_edge(source_node, target_node):
        return MapEdge.objects.create(
            source=source_node,
            target=target_node,
            created_at=timezone.now()
        )

    @staticmethod
    def list_edges_by_repo(repo_id):
        return MapEdge.objects.filter(
            source__repo_file__repository_id=repo_id,
            target__repo_file__repository_id=repo_id
        )

    @staticmethod
    def delete_edge(edge_id):
        edge = get_object_or_404(MapEdge, id=edge_id)
        edge.delete()
