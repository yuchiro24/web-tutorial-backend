from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def get_header(self, request: Request):
        print("cookies", request.COOKIES)
        token = request.COOKIES.get('access_token')
        request.META["HTTP_AUTHORIZATION"] = "{header_type} {access_token}".format(
            header_type="Bearer", access_token=token
        )
        refresh = request.COOKIES.get('refresh_token')
        request.META["HTTP_REFRESH_TOKEN"] = "{header_type} {refresh_token}".format(
            header_type="Bearer", refresh_token=refresh
        )
        return super().get_header(request)
