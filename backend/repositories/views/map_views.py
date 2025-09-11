#repositories/views/map_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from repositories.services.map_service import extract_import_lines_for_repo, resolve_import_links
from repositories.models import FileContent

class RepoMapPreviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, repo_id):
        import_map = extract_import_lines_for_repo(repo_id)

        resolved_links = resolve_import_links(repo_id, import_map)

        file_contents = FileContent.objects.filter(repo_file__repository_id=repo_id).select_related("repo_file")
        nodes = [{"id": fc.repo_file.path, "label": fc.repo_file.file_name or fc.repo_file.path} for fc in file_contents]

        edges = []
        for source, targets in resolved_links.items():
            for target in targets:
                edges.append({"source": source, "target": target})

        return Response({
            "nodes": nodes,
            "edges": edges
        })
