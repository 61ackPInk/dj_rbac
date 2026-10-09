"""
-*- coding: utf-8 -*-
@File  : permissions.py
@Author: 61ackPink
@Time : 2026/9/28 16:57
@Desc : 操作权限管理视图
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import Permission
from apps.users.serializers import PermissionSerializer
from common.permissions import IsRootUser


class PermissionListCreateAPIView(GenericAPIView):
    """操作权限列表与创建接口"""

    serializer_class = PermissionSerializer

    # 权限定义会影响整个系统的安全，
    # 暂时只允许根管理员维护
    permission_classes = [
        IsRootUser,
    ]

    def get_queryset(self):
        """
        查询权限及所属页面。

        select_related("page") 可以避免序列化每条
        权限时再次单独查询页面。
        """

        return Permission.objects.select_related(
            "page",
        )

    def get(self, request, *args, **kwargs):
        """查询全部操作权限，包括已经停用的权限"""

        permissions = self.get_queryset()

        serializer = self.get_serializer(
            permissions,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """创建一条操作权限"""

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        permission = serializer.save()

        # 重新查询所属页面，
        # 确保响应数据包含完整页面信息
        permission = self.get_queryset().get(
            id=permission.id,
        )

        response_serializer = self.get_serializer(
            permission,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PermissionDetailAPIView(GenericAPIView):
    """操作权限详情、修改和停用接口"""

    serializer_class = PermissionSerializer
    permission_classes = [
        IsRootUser,
    ]

    def get_queryset(self):
        """查询权限及其所属页面"""

        return Permission.objects.select_related(
            "page",
        )

    def get_object(self):
        """根据路由中的 permission_id 查询权限"""

        permission_id = self.kwargs[
            "permission_id"
        ]

        return get_object_or_404(
            self.get_queryset(),
            id=permission_id,
        )

    def get(self, request, *args, **kwargs):
        """获取指定权限的详细信息"""

        permission = self.get_object()

        serializer = self.get_serializer(
            permission,
        )

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """局部修改指定操作权限"""

        permission = self.get_object()

        serializer = self.get_serializer(
            permission,
            data=request.data,

            # PATCH 只需要提交需要修改的字段
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        permission = serializer.save()

        permission = self.get_queryset().get(
            id=permission.id,
        )

        response_serializer = self.get_serializer(
            permission,
        )

        return Response(
            response_serializer.data,
        )

    def delete(self, request, *args, **kwargs):
        """
        停用操作权限。

        不真正删除数据库记录，
        避免破坏角色与权限之间的历史关系。
        """

        permission = self.get_object()

        permission.is_active = False

        permission.save(
            update_fields=[
                "is_active",
                "update_time",
            ],
        )

        return Response({
            "id": permission.id,
            "name": permission.name,
            "code": permission.code,
            "is_active": permission.is_active,
            "message": "操作权限已停用",
        })