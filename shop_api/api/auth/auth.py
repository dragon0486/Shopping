from rest_framework.authentication import BaseAuthentication
from api import models
from rest_framework import exceptions

class Authentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        token_obj = models.UserAuthToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("验证失败!")  # 验证失败抛出的异常会返回到页面
        return (token_obj.user, token_obj)