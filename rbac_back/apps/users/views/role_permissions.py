"""
-*- coding: utf-8 -*-
@File  : role_permissions.py
@Author: 61ackPink
@Time : 2026/9/28 17:18
@Desc : 角色操作权限分配视图
"""

from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.serializers import (
    RolePermissionAssignSerializer,
    RoleSerializer,
)
from common.permissions import IsRootUser


class RolePermissionAssignAPIView(
    GenericAPIView
):
    """查询和修改角色的操作权限"""

    serializer_class = (
        RolePermissionAssignSerializer
    )

    # 给角色分配权限属于高风险操作，
    # 只允许根管理员执行
    permission_classes = [
        IsRootUser,
    ]

    def get_queryset(self):
        """
        查询角色及其操作权限。

        permissions__page 表示同时预加载
        权限以及权限所属页面。
        """

        return Role.objects.prefetch_related(
            "permissions__page",
            "pages",
        )

    def get_object(self):
        """根据 role_id 查询角色"""

        role_id = self.kwargs["role_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=role_id,
        )

    def get(self, request, *args, **kwargs):
        """查询指定角色当前拥有的权限"""

        role = self.get_object()

        serializer = RoleSerializer(role)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        替换指定角色的全部操作权限。

        即使使用 PATCH，
        permission_ids 也必须提交。
        提交空数组表示清空角色全部操作权限。
        """

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,

            # 不使用 partial=True，
            # 确保 permission_ids 必须提交
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        role = serializer.save()

        # 重新查询，避免返回修改前的预加载缓存
        role = self.get_queryset().get(
            id=role.id,
        )

        response_serializer = RoleSerializer(
            role,
        )

        return Response(
            response_serializer.data,
        )