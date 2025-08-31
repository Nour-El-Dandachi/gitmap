import os
import requests

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from social_django.utils import psa

from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer
from utils.response import responseJSON
from utils.tokens import get_custom_tokens_for_user


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_custom_tokens_for_user(user)

            return responseJSON({
                "message": "User created successfully",
                "tokens": tokens
            })

        return responseJSON({"error": "Invalid credentials"}, status="error", status_code=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = get_custom_tokens_for_user(user)

            return responseJSON({
                "message": "Login successful",
                "tokens": tokens
            })

        return responseJSON(serializer.errors, status="error", status_code=400)


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

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,

            "code": code,
        },
        headers={"Accept": "application/json"},
    )
    access_token = token_response.json().get("access_token")

    if not access_token:
        return responseJSON({"error": "GitHub token error"}, status="error", status_code=400)

    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"}
    )
    github_user = user_response.json()

    github_email = github_user.get("email")
    if not github_email:
        emails_response = requests.get(
            "https://api.github.com/user/emails",
            headers={"Authorization": f"token {access_token}"}
        )
        emails_data = emails_response.json()
        primary = next((e for e in emails_data if e.get("primary") and e.get("verified")), None)
        github_email = primary["email"] if primary else None

    user, _ = User.objects.get_or_create(
        github_id=github_user["id"],
        defaults={
            "name": github_user.get("name") or github_user.get("login"),
            "email": github_email,
            "github_login": github_user.get("login"),
            "github_token": access_token,
        }
    )

    tokens = get_custom_tokens_for_user(user)

    return JsonResponse({
        "status": "success",
        "payload": {
            "message": "GitHub login successful",
            "tokens": tokens
        }
    })

