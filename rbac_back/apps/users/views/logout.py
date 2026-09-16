"""
-*- coding: utf-8 -*-
@File  : logout.py
@Author: 61ackPink
@Time : 2026/9/16
@Desc : 退出登录
"""
from django.db.models import F
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User


class UserLogoutAPIView(GenericAPIView):
    """退出当前用户的所有登录状态"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        递增 Token 版本，使此前签发的全部 Token 失效。

        使用数据库表达式原子更新，避免同一用户同时发起多个
        退出请求时发生 Token 版本更新丢失。
        """

        User.objects.filter(
            id=request.user.id,
        ).update(
            token_version=F("token_version") + 1,
        )

        return Response({
            "message": "退出登录成功",
        })
