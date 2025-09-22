# services/auth_service.py
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from ..serializers import UserLoginSerializer, UserRegisterSerializer
from utils.tokens import get_custom_tokens_for_user

class AuthService:

    @staticmethod
    def login(request):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        tokens = get_custom_tokens_for_user(user)

        return {
            "message": "Login successful",
            "tokens": tokens
        }

    @staticmethod
    def register(request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_custom_tokens_for_user(user)

        return {
            "message": "User created successfully",
            "tokens": tokens
        }
