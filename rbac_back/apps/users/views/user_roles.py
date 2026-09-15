"""
-*- coding: utf-8 -*-
@File  : user_roles.py
@Author: 61ackPink
@Time : 2026/9/15 15:12
@Desc : 角色分配视图
"""
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    UserInfoSerializer,
    UserRoleAssignSerializer,
)
from common.permissions import IsRootUser


class UserRoleAssignAPIView(GenericAPIView):
    """给用户分配或取消角色"""

    serializer_class = UserRoleAssignSerializer

    # 只有根管理员能够分配用户角色
    permission_classes = [IsRootUser]

    def get_object(self):
        """
        根据路由中的 user_id 查询用户。

        使用 select_related("role") 可以在同一次查询中
        读取用户和角色，减少后续数据库查询。
        """

        user_id = self.kwargs["user_id"]

        return get_object_or_404(
            User.objects.select_related("role"),
            id=user_id,
        )

    def patch(self, request, *args, **kwargs):
        """修改用户的角色"""

        user = self.get_object()

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 修改后重新读取角色关系，
        # 确保返回的是最新角色数据
        user = User.objects.select_related("role").get(
            id=user.id
        )

        # 使用统一的用户信息序列化器返回结果
        response_serializer = UserInfoSerializer(user)

        return Response(response_serializer.data)