from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from repositories.models import Repository

User = get_user_model()


class WatchedReposSummaryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="nour@example.com",
            password="password",
            name="Nour"
        )
        self.url = "/api/notifications/watched-repos-summary/"

    def test_empty_summary(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"], {})

    def test_watched_repo_summary(self):
        repo = Repository.objects.create(
            user=self.user,
            name="gitmap",
            owner="nour",
            is_watched=True,
            branch="main",
            metadata={"last_sha": "abc123"}
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")

        payload = response.data["payload"]
        self.assertIn(self.user.id, payload)
        repos = payload[self.user.id]
        self.assertEqual(len(repos), 1)

        repo_data = repos[0]
        self.assertEqual(repo_data["repo_id"], repo.id)
        self.assertEqual(repo_data["repo"], "nour/gitmap")
        self.assertEqual(repo_data["branch"], "main")
        self.assertEqual(repo_data["last_sha"], "abc123")
