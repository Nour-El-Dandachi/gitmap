from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from utils.response import responseJSON
from rest_framework_simplejwt.tokens import RefreshToken

def get_custom_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    refresh["name"] = user.name
    refresh["email"] = user.email
    refresh["role"] = user.role

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

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