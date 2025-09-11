#/views/repo_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from repositories.services.repo_service import RepoService
from utils.response import responseJSON
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from repositories.serializers import RepositorySerializer

class UserRepositoriesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repos = RepoService.get_user_repositories(request.user)
        serializer = RepositorySerializer(repos, many=True)
        return Response(
            {"status": "success", "payload": serializer.data},
            status=status.HTTP_200_OK
        )


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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from repositories.models import Repository
from utils.response import responseJSON

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from repositories.models import Repository
from utils.response import responseJSON

class UpdateLastShaView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        repo_id = request.data.get("repo_id")
        new_sha = request.data.get("new_sha")

        if not repo_id or not new_sha:
            return responseJSON({"error": "Missing parameters"}, status="error", status_code=400)

        try:
            repo = Repository.objects.get(id=repo_id)
        except Repository.DoesNotExist:
            return responseJSON({"error": "Repository not found"}, status="error", status_code=404)

        metadata = repo.metadata or {}
        metadata["last_sha"] = new_sha
        repo.metadata = metadata
        repo.save(update_fields=["metadata"])

        return responseJSON({"message": "last_sha updated successfully"})
