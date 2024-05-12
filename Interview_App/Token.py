from django.contrib.auth.backends import BaseBackend
from .models import AuthToken

class TokenAuthenticationBackend(BaseBackend):
    def authenticate(self, request, token=None):
        try:
            auth_token = AuthToken.objects.get(token=token, is_active=True)
            return auth_token.user
        except AuthToken.DoesNotExist:
            return None
