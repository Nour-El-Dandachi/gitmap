# map/views/map_views.py
from map.services.map_service import MapService
from map.serializers import NodePositionSerializer, FileEdgeSerializer
from utils.response import responseJSON

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from map.serializers import NodePositionSerializer, FileEdgeSerializer

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from map.models import NodePosition, FileEdge
from repositories.models import RepoFile

from map.serializers import NodePositionReadSerializer, FileEdgeReadSerializer

class NodePositionListCreateView(APIView):
    def get(self, request):
        nodes = MapService.get_all_node_positions()
        serializer = NodePositionSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        is_bulk = isinstance(data, list)

        try:
            if is_bulk:
                serializer = NodePositionSerializer(data=data, many=True)
            else:
                serializer = NodePositionSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FileEdgeListCreateView(APIView):
    def get(self, request):
        edges = MapService.get_all_file_edges()
        serializer = FileEdgeSerializer(edges, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        is_bulk = isinstance(data, list)

        try:
            if is_bulk:
                serializer = FileEdgeSerializer(data=data, many=True)
            else:
                serializer = FileEdgeSerializer(data=data)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


class MapDataView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get code map data",
        operation_description="Fetches the code map (nodes and edges) for a repository. Requires Bearer token authentication.",
        manual_parameters=[
            openapi.Parameter(
                "repo_id",
                openapi.IN_PATH,
                description="Repository ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "nodes": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="List of nodes representing repository files",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "file_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=352),
                                "file_name": openapi.Schema(type=openapi.TYPE_STRING, example="ViewCapsuleController.php"),
                                "x": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=160.0),
                                "y": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=180.0),
                            },
                        ),
                    ),
                    "edges": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="List of edges representing dependencies between files",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "source": openapi.Schema(type=openapi.TYPE_INTEGER, example=353),
                                "target": openapi.Schema(type=openapi.TYPE_INTEGER, example=352),
                            },
                        ),
                    ),
                },
            ),
            401: openapi.Response("Unauthorized"),
        },
    )
    def get(self, request, repo_id):
        repo_file_ids = RepoFile.objects.filter(repository_id=repo_id).values_list("id", flat=True)

        nodes = NodePosition.objects.filter(repo_file_id__in=repo_file_ids).select_related("repo_file")
        edges = FileEdge.objects.filter(
            source_id__in=repo_file_ids,
            target_id__in=repo_file_ids
        )

        serialized_nodes = NodePositionReadSerializer(nodes, many=True).data
        serialized_edges = FileEdgeReadSerializer(edges, many=True).data

        return Response({
            "nodes": serialized_nodes,
            "edges": serialized_edges
        })
