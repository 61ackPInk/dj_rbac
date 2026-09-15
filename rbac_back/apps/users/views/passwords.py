"""
-*- coding: utf-8 -*-
@File  : passwords.py
@Author: 61ackPink
@Time : 2026/9/15 17:32
@Desc : 修改密码
"""
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    UserPasswordChangeSerializer,
    UserPasswordResetSerializer,
)
from common.permissions import IsRootUser
from common.utils.jwt import (
    create_access_token,
    create_refresh_token,
)


class UserPasswordChangeAPIView(GenericAPIView):
    """当前用户修改自己的密码"""

    serializer_class = UserPasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """验证原密码并修改为新密码"""

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 密码修改后 token_version 已经变化，
        # 旧 Token 全部失效，因此签发一组新 Token
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        expires_in = (
            settings.JWT_AUTH[
                "ACCESS_TOKEN_LIFETIME_MINUTES"
            ]
            * 60
        )

        return Response({
            "message": "密码修改成功",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": expires_in,
        })


class UserPasswordResetAPIView(GenericAPIView):
    """根管理员重置指定用户密码"""

    serializer_class = UserPasswordResetSerializer
    permission_classes = [IsRootUser]

    def get_object(self):
        """根据路由中的 user_id 查询用户"""

        user_id = self.kwargs["user_id"]

        return get_object_or_404(
            User,
            id=user_id,
        )

    def patch(self, request, *args, **kwargs):
        """重置指定普通用户的密码"""

        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "id": user.id,
            "username": user.username,
            "message": "用户密码重置成功",
        })