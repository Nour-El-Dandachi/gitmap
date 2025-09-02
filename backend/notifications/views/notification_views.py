# notifications/views/notification_views.py
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from notifications.services.notification_service import NotificationService
from notifications.serializers.notification_serializer import NotificationSerializer
from utils.response import responseJSON

class NotificationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = NotificationService.list_for_user(request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return responseJSON(serializer.data)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            notification = NotificationService.create(
                user=request.user,
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
