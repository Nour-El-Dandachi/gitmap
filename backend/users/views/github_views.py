# views/github_views.py

from ..services.github_auth_service import GitHubAuthService
from django.http import JsonResponse
import os
from django.shortcuts import redirect
from utils.response import responseJSON
from utils.tokens import get_custom_tokens_for_user

GITHUB_CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")
FRONTEND_REDIRECT_URL = "http://localhost:3000/home"  # adjust this

def github_redirect(request):
    redirect_uri = "http://localhost:8000/auth/github/callback/"
    github_url = (
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=user"
    )
    return redirect(github_url)

def github_callback(request):
    code = request.GET.get("code")
    if not code:
        return responseJSON({"error": "Missing code from GitHub"}, status="error", status_code=400)

    access_token = GitHubAuthService.exchange_code_for_token(code)
    if not access_token:
        return responseJSON({"error": "GitHub token error"}, status="error", status_code=400)

    github_user = GitHubAuthService.fetch_github_user(access_token)
    github_email = github_user.get("email") or GitHubAuthService.fetch_primary_email(access_token)
    user = GitHubAuthService.login_or_register_github_user(github_user, github_email, access_token)

    tokens = get_custom_tokens_for_user(user)
    return JsonResponse({
        "status": "success",
        "payload": {
            "message": "GitHub login successful",
            "tokens": tokens
        }
    })
