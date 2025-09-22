# repositories/views/map_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from repositories.services.map_service import build_file_imports
from repositories.models import Repository

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


class RepoMapExistsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_id):
        exists = Repository.objects.filter(id=repo_id, has_map=True).exists()
        return Response({"exists": exists})
