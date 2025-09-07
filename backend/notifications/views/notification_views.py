# notifications/views/notification_views.py
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from notifications.services.notification_service import NotificationService
from notifications.serializers.notification_serializer import NotificationSerializer
from utils.response import responseJSON
from rest_framework.permissions import AllowAny 

from repositories.models import Repository
from rest_framework.response import Response

class NotificationListCreateView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        notifications = NotificationService.list_for_user(request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return responseJSON(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = NotificationService.create(
                user=serializer.validated_data['user'],
                title=serializer.validated_data['title'],
                message=serializer.validated_data['message']
            )
            return responseJSON(NotificationSerializer(notification).data, status_code=status.HTTP_201_CREATED)
        return responseJSON(serializer.errors, status="error", status_code=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        notification = NotificationService.get(request.user, pk)
        serializer = NotificationSerializer(notification)
        return responseJSON(serializer.data)

class DeleteNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        NotificationService.delete(request.user, pk)
        return responseJSON({"detail": "Notification deleted."}, status_code=status.HTTP_204_NO_CONTENT)

class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        notification = NotificationService.mark_as_read(request.user, pk)
        return responseJSON(NotificationSerializer(notification).data)

class MarkAllAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        NotificationService.mark_all_as_read(request.user)
        return responseJSON({"detail": "All notifications marked as read."})


class WatchedReposSummaryView(APIView):
    permission_classes = []

    def get(self, request):
        repos = Repository.objects.filter(is_watched=True).select_related("user")
        result = {}

        for repo in repos:
            user_id = repo.user.id
            if user_id not in result:
                result[user_id] = []

            result[user_id].append({
                "repo_id": repo.id,
                "repo": f"{repo.owner}/{repo.name}",
                "branch": repo.branch or repo.default_branch or "main",
                "last_sha": (repo.metadata or {}).get("last_sha", "")
            })

        return responseJSON(result)
