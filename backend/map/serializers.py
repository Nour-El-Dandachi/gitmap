from rest_framework import serializers
from map.models import NodePosition, FileEdge
from repositories.models import RepoFile

class NodePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodePosition
        fields = ['id', 'repo_file', 'x', 'y']

class FileEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileEdge
        fields = ['id', 'source', 'target']
