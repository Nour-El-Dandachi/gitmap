# views/auth_views.py
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from utils.response import responseJSON
from ..services.auth_service import AuthService

from rest_framework.exceptions import APIException

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = AuthService.login(request)
            return responseJSON(data)
        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=400)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = AuthService.register(request)
            return responseJSON(data)
        except Exception as e:
            return responseJSON({"error": str(e)}, status="error", status_code=400)
