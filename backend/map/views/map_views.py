# map/views/map_views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from map.services.map_service import MapService
from map.serializers import MapNodeSerializer, MapEdgeSerializer
from utils.response import responseJSON


class MapNodeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_file_id):
        nodes = MapService.list_nodes(repo_file_id)
        serializer = MapNodeSerializer(nodes, many=True)
        return responseJSON(serializer.data)

    def post(self, request):
        serializer = MapNodeSerializer(data=request.data)
        if serializer.is_valid():
            node = MapService.create_node(serializer.validated_data)
            return responseJSON(MapNodeSerializer(node).data, status_code=status.HTTP_201_CREATED)
        return responseJSON(serializer.errors, status="error", status_code=status.HTTP_400_BAD_REQUEST)


class MapEdgeListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_file_id):
        edges = MapService.list_edges(repo_file_id)
        serializer = MapEdgeSerializer(edges, many=True)
        return responseJSON(serializer.data)

    def post(self, request):
        serializer = MapEdgeSerializer(data=request.data)
        if serializer.is_valid():
            edge = MapService.create_edge(serializer.validated_data)
            return responseJSON(MapEdgeSerializer(edge).data, status_code=status.HTTP_201_CREATED)
        return responseJSON(serializer.errors, status="error", status_code=status.HTTP_400_BAD_REQUEST)


class MapNodeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        MapService.delete_node(pk)
        return responseJSON({"detail": "Node deleted."}, status_code=status.HTTP_204_NO_CONTENT)


class MapEdgeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        MapService.delete_edge(pk)
        return responseJSON({"detail": "Edge deleted."}, status_code=status.HTTP_204_NO_CONTENT)
