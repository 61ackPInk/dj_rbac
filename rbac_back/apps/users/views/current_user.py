"""
-*- coding: utf-8 -*-
@File  : current_user.py
@Author: 61ackPink
@Time : 2026/9/11 16:22
@Desc : 当前用户信息视图
"""
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    CurrentUserInfoSerializer,
    UserProfileUpdateSerializer,
)


class CurrentUserAPIView(GenericAPIView):
    """
    获取和修改当前登录用户信息。

    GET：
        返回当前登录用户信息；
        同时返回当前用户的操作权限编码。

    PATCH：
        当前用户修改自己的用户名或邮箱。
    """

    serializer_class = CurrentUserInfoSerializer

    # 当前接口只要求用户已经登录
    permission_classes = [
        IsAuthenticated,
    ]

    def get_serializer_class(self):
        """根据请求方法选择序列化器"""

        if self.request.method == "PATCH":
            return UserProfileUpdateSerializer

        return CurrentUserInfoSerializer

    def get_current_user(self):
        """
        重新查询当前登录用户及其角色。

        JWT 身份认证已经得到 request.user，
        但没有提前加载角色。

        使用 select_related("role") 后，
        获取 user.role 时不需要再次查询数据库。
        """

        return User.objects.select_related(
            "role",
        ).get(
            id=self.request.user.id,
        )

    def get(self, request, *args, **kwargs):
        """获取当前登录用户及操作权限"""

        user = self.get_current_user()

        serializer = self.get_serializer(
            user,
        )

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """修改当前用户的用户名或邮箱"""

        user = self.get_current_user()

        serializer = self.get_serializer(
            user,
            data=request.data,

            # 只需要提交发生修改的字段
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        # 修改完成后重新查询角色信息，
        # 再使用当前用户专用序列化器返回权限
        user = User.objects.select_related(
            "role",
        ).get(
            id=user.id,
        )

        response_serializer = (
            CurrentUserInfoSerializer(user)
        )

        return Response(
            response_serializer.data,
        )