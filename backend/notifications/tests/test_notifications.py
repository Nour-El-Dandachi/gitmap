from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()


class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="nour@example.com",
            password="password",
            name="Nour"
        )
        self.client.force_authenticate(user=self.user)

        self.list_url = "/api/notifications/"
        self.mark_all_url = "/api/notifications/mark-all-read/"

    def test_create_notification(self):
        data = {
            "user": self.user.id,
            "title": "Test Notification",
            "message": "This is a test message"
        }
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["title"], "Test Notification")
        self.assertEqual(Notification.objects.count(), 1)

    def test_list_notifications(self):
        Notification.objects.create(
            user=self.user,
            title="Hello",
            message="World"
        )
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(len(response.data["payload"]), 1)

    def test_mark_as_read(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Read me",
            message="Mark as read"
        )
        url = f"/api/notifications/{notification.id}/mark-read/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_mark_all_as_read(self):
        Notification.objects.create(user=self.user, title="One", message="Test1")
        Notification.objects.create(user=self.user, title="Two", message="Test2")

        response = self.client.post(self.mark_all_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")

        unread_count = Notification.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(unread_count, 0)

    def test_delete_notification(self):
        notification = Notification.objects.create(
            user=self.user,
            title="Delete me",
            message="To be deleted"
        )
        url = f"/api/notifications/{notification.id}/delete/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Notification.objects.count(), 0)
