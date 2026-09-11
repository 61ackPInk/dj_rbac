"""
-*- coding: utf-8 -*-
@File  : refresh_token.py
@Author: 61ackPink
@Time : 2026/9/11 16:42
@Desc : Token 刷新视图
"""
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import RefreshTokenSerializer
from common.utils.jwt import create_access_token


class RefreshTokenAPIView(GenericAPIView):
    """刷新访问令牌接口"""

    serializer_class = RefreshTokenSerializer

    # access_token 过期后用户已经无法通过普通身份认证，
    # 所以该接口允许匿名请求，再由序列化器验证 refresh_token
    permission_classes = [AllowAny]

    # 不执行默认的 JWTAuthentication
    # 否则请求头里过期的 access_token 可能导致请求提前失败
    authentication_classes = []

    def post(self, request):
        """
        使用 refresh_token 换取新的 access_token。
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 序列化器已经验证了 refresh_token 并查询了用户
        user = serializer.validated_data["user"]

        # 为用户生成新的短期访问令牌
        access_token = create_access_token(user)

        access_expires = (
            settings.JWT_AUTH["ACCESS_TOKEN_LIFETIME_MINUTES"]
            * 60
        )

        return Response({
            "access_token": access_token,
            "token_type": "Bearer",
            "expires_in": access_expires,
        })