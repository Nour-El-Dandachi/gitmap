from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from .serializers import UserLoginSerializer
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
