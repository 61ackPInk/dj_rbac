"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/15 15:31
@Desc : 用户列表视图
"""
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserInfoSerializer
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