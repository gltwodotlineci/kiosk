from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import DeviceTokenAuthentication

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            keyword, token = auth_header.split(' ')
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format.')

        try:
            token_obj = DeviceTokenAuthentication.objects.get(key=token)
        except DeviceTokenAuthentication.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (None, token_obj)
