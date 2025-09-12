# repositories/views/map_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from repositories.services.map_service import build_file_imports

class RepoFileImportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_id):
        files_with_imports = build_file_imports(repo_id)
        return Response(files_with_imports)

from repositories.services.map_algorithm import build_code_map

class RepoMapView(APIView):
    def get(self, request, repo_id):
        result = build_code_map(repo_id)
        return Response(result)
