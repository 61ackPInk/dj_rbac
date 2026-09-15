"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/15 15:31
@Desc : 用户视图
"""
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    UserInfoSerializer,
    UserAdminUpdateSerializer,
)
from common.permissions import IsRootUser


class UserListAPIView(GenericAPIView):
    """获取系统用户列表"""
    serializer_class = UserInfoSerializer

    # 用户列表包含邮箱、角色等信息，
    # 暂时只允许根管理员查看
    permission_classes = [IsRootUser]

    def get(self, request, *args, **kwargs):
        """获取所有用户及其角色"""

        # select_related("role") 会通过联表查询
        # 一次性获得用户及其角色，避免逐个查询角色
        users = User.objects.select_related("role").order_by(
            "id"
        )

        # many=True 表示当前序列化的是多个用户
        serializer = self.get_serializer(
            users,
            many=True,
        )

        return Response(serializer.data)

class UserDetailAPIView(GenericAPIView):
    """用户详情与用户信息管理接口"""

    serializer_class = UserAdminUpdateSerializer
    permission_classes = [IsRootUser]

    def get_object(self):
        """根据路由中的 user_id 查询用户"""

        user_id = self.kwargs["user_id"]

        return get_object_or_404(
            User.objects.select_related("role"),
            id=user_id,
        )

    def get_serializer_class(self):
        """
        GET 使用只读用户信息序列化器；
        PATCH 使用管理员修改序列化器。
        """

        if self.request.method == "GET":
            return UserInfoSerializer

        return UserAdminUpdateSerializer

    def get(self, request, *args, **kwargs):
        """获取指定用户详情"""

        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """修改指定用户的基本信息"""

        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,

            # 允许只提交需要修改的字段
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 使用只读序列化器返回完整用户信息
        response_serializer = UserInfoSerializer(user)

        return Response(response_serializer.data)

