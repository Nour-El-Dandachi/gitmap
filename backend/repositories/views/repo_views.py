#/views/repo_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from repositories.services.repo_service import RepoService
from utils.response import responseJSON
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

class FetchTreeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            url = request.data.get("url")
            if not url:
                return responseJSON({"error": "Repository URL is required."}, status="error", status_code=400)

            data = RepoService.fetch_tree(url)
            return Response(data)
        except ValueError as e:
            return responseJSON({"error": str(e)}, status="error", status_code=400)
        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=500)


class FetchFileContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, owner, repo, sha):
        try:
            data = RepoService.fetch_file_content(owner, repo, sha)
            return responseJSON(data)
        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=500)

class AddRepositoryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            url = request.data.get("url")
            branch = request.data.get("branch", "main")

            if not url:
                return responseJSON({"error": "Repository URL is required."}, status="error", status_code=400)

            repo = RepoService.start_indexing_workflow(user=request.user, url=url, branch=branch)

            return responseJSON({
                "message": "Indexing started.",
                "repo_id": repo.id,
                "repo_name": repo.name
            }, status="success")

        except ValueError as e:
            return responseJSON({"error": str(e)}, status="error", status_code=400)
        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=500)
