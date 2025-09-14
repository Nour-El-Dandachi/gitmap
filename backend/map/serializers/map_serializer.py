from rest_framework import serializers
from map.models import MapNode, MapEdge
from repositories.models import RepoFile

class RepoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoFile
        fields = ["id", "file_name", "path"]

class MapNodeSerializer(serializers.ModelSerializer):
    repo_file = RepoFileSerializer()

    class Meta:
        model = MapNode
        fields = ["id", "repo_file", "x", "y", "created_at", "updated_at"]

class MapEdgeSerializer(serializers.ModelSerializer):
    source = MapNodeSerializer()
    target = MapNodeSerializer()

    class Meta:
        model = MapEdge
        fields = ["id", "source", "target", "created_at"]
