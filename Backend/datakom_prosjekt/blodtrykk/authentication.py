# your_app/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication

#The custom authentication class that uses cookies instead of a header. 
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from the cookie
        raw_token = request.COOKIES.get('access') or None
        if raw_token is None:
            header = self.get_header(request)
            if header is not None:
                raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
