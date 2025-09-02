# services/github_auth_service.py

import os, requests
from users.models import User
from utils.tokens import get_custom_tokens_for_user

class GitHubAuthService:

    @staticmethod
    def exchange_code_for_token(code):
        GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
        GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

        token_response = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        return token_response.json().get("access_token")

    @staticmethod
    def fetch_github_user(access_token):
        user_response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {access_token}"}
        )
        return user_response.json()

    @staticmethod
    def fetch_primary_email(access_token):
        emails_response = requests.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
        )
        emails_data = emails_response.json()
        primary = next((e for e in emails_data if e.get("primary") and e.get("verified")), None)
        return primary["email"] if primary else None

    @staticmethod
    def login_or_register_github_user(github_user, github_email, access_token):
        user, _ = User.objects.get_or_create(
            github_id=github_user["id"],
            defaults={
                "name": github_user.get("name") or github_user.get("login"),
                "email": github_email,
                "github_login": github_user.get("login"),
                "github_token": access_token,
            }
        )
        return user
