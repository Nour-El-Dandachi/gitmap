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