# map/views/map_views.py
from map.services.map_service import MapService
from map.serializers import NodePositionSerializer, FileEdgeSerializer
from utils.response import responseJSON

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from map.serializers import NodePositionSerializer, FileEdgeSerializer

class NodePositionListCreateView(APIView):
    def get(self, request):
        nodes = MapService.get_all_node_positions()
        serializer = NodePositionSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            node = MapService.create_node_position(
                repo_file_id=data["repo_file"],
                x=data["x"],
                y=data["y"]
            )
            return Response(NodePositionSerializer(node).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FileEdgeListCreateView(APIView):
    def get(self, request):
        edges = MapService.get_all_file_edges()
        serializer = FileEdgeSerializer(edges, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        try:
            edge = MapService.create_file_edge(
                source_id=data["source"],
                target_id=data["target"]
            )
            return Response(FileEdgeSerializer(edge).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
