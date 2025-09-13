# repositories/views/map_ai_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from repositories.services.map_ai_service import generate_map_with_ai

# class RepoMapAIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, repo_id):
#         graph = generate_map_with_ai(repo_id)
#         return Response(graph)


from repositories.services.map_service import get_key_files_for_map
from repositories.services.map_service import get_codebase_dependency_table

class ImportantFilesForMapView(APIView):
    def get(self, request, repo_id):
        result = get_key_files_for_map(repo_id)
        return Response(result)

class RepoMapAIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_id):
        result = get_codebase_dependency_table(repo_id)
        return Response(result)
