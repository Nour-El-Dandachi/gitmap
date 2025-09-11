# notifications/services/notification_service.py
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from django.utils import timezone

class NotificationService:

    @staticmethod
    def create(user, title, message):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            is_read=False,
            created_at=timezone.now()
        )

    @staticmethod
    def list_for_user(user):
        return Notification.objects.filter(user=user).order_by('-created_at')

    @staticmethod
    def get(user, notification_id):
        return get_object_or_404(Notification, id=notification_id, user=user)

    @staticmethod
    def mark_as_read(user, notification_id):
        notification = NotificationService.get(user, notification_id)
        notification.is_read = True
        notification.save()
        return notification

    @staticmethod
    def mark_all_as_read(user):
        return Notification.objects.filter(user=user, is_read=False).update(is_read=True)

    @staticmethod
    def delete(user, notification_id):
        notification = NotificationService.get(user, notification_id)
        notification.delete()
        return True

