from rest_framework import exceptions
from API import models
from rest_framework.authentication import BaseAuthentication


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        token = request._request.GET.get("token")
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        # 在rest_framework内部会将这两个字段赋值给request,以供后续操作使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, request):
        pass