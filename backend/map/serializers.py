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

class NodePositionReadSerializer(serializers.ModelSerializer):
    file_id = serializers.IntegerField(source="repo_file.id")
    file_name = serializers.CharField(source="repo_file.file_name")

    class Meta:
        model = NodePosition
        fields = ['file_id', 'file_name', 'x', 'y']

class FileEdgeReadSerializer(serializers.ModelSerializer):
    source = serializers.IntegerField(source='source.id')
    target = serializers.IntegerField(source='target.id')

    class Meta:
        model = FileEdge
        fields = ["source", "target"]
