from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch
from repositories.models import Repository

User = get_user_model()


class RepositoryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="nour@example.com",
            password="password",
            name="Nour"
        )
        self.client.force_authenticate(user=self.user)

        self.list_url = "/api/repos/user/"
        self.add_url = "/api/repos/add/"
        self.tree_url = "/api/repos/tree/"
        self.update_sha_url = "/api/repos/update-sha/"
        self.file_content_url = "/api/repos/content/nour/gitmap/abc123/"

    def test_user_repositories_empty(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["payload"], [])

    @patch("repositories.services.repo_service.RepoService.start_indexing_workflow")
    def test_add_repository_success(self, mock_start_indexing):
        # Mock RepoService to avoid hitting GitHub API
        fake_repo = Repository(id=1, user=self.user, name="gitmap", owner="nour")
        mock_start_indexing.return_value = fake_repo

        response = self.client.post(self.add_url, {"url": "https://github.com/nour/gitmap"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("repo_id", response.data["payload"])

    def test_add_repository_missing_url(self):
        response = self.client.post(self.add_url, {"url": ""}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")

    @patch("repositories.services.repo_service.RepoService.fetch_tree")
    def test_fetch_tree_success(self, mock_fetch_tree):
        mock_fetch_tree.return_value = {"tree": [{"path": "README.md"}]}
        response = self.client.post(self.tree_url, {"url": "https://github.com/nour/gitmap"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("tree", response.data)

    def test_fetch_tree_missing_url(self):
        response = self.client.post(self.tree_url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["status"], "error")

    def test_update_last_sha_success(self):
        repo = Repository.objects.create(
            user=self.user,
            owner="nour",
            name="gitmap",
            url="https://github.com/nour/gitmap",
            is_watched=True
        )
        response = self.client.post(
            self.update_sha_url,
            {"repo_id": repo.id, "new_sha": "abc123"},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        repo.refresh_from_db()
        self.assertEqual(repo.metadata.get("last_sha"), "abc123")

    def test_update_last_sha_repo_not_found(self):
        response = self.client.post(
            self.update_sha_url,
            {"repo_id": 999, "new_sha": "abc123"},
            format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["status"], "error")

    @patch("repositories.services.repo_service.RepoService.fetch_file_content")
    def test_fetch_file_content_success(self, mock_fetch_file_content):
        mock_fetch_file_content.return_value = {"content": "print('hello')"}
        response = self.client.get(self.file_content_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("content", response.data["payload"])
