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

from apps.users.serializers import (
    UserInfoSerializer,
    UserProfileUpdateSerializer,
)


class CurrentUserAPIView(GenericAPIView):
    """获取和修改当前登录用户信息"""

    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        GET：返回用户完整信息
        PATCH：验证允许修改的个人资料
        """

        if self.request.method == "PATCH":
            return UserProfileUpdateSerializer

        return UserInfoSerializer

    def get(self, request, *args, **kwargs):
        """获取当前登录用户信息"""

        serializer = self.get_serializer(
            request.user
        )

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """修改当前用户的用户名或邮箱"""

        serializer = self.get_serializer(
            request.user,
            data=request.data,

            # 允许只提交需要修改的字段
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 修改成功后使用只读序列化器
        # 返回完整的用户信息
        response_serializer = UserInfoSerializer(user)

        return Response(response_serializer.data)