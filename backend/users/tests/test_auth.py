from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.email = "nour@example.com"
        self.password = "password"
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            name="Nour El Dandachi"
        )

        self.login_url = "/api/users/auth/login/"
        self.register_url = "/api/users/auth/register/"

    def test_login_success(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["message"], "Login successful")
        self.assertIn("access", response.data["payload"]["tokens"])
        self.assertIn("refresh", response.data["payload"]["tokens"])

    def test_login_fail_wrong_password(self):
        data = {
            "email": self.email,
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")

    def test_register_success(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "name": "New User",
        }
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"]["message"], "User created successfully")
        self.assertIn("access", response.data["payload"]["tokens"])
        self.assertIn("refresh", response.data["payload"]["tokens"])

        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_fail_duplicate_email(self):
        data = {
            "email": self.email,
            "password": "somepassword",
            "name": "Duplicate User",
        }
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
