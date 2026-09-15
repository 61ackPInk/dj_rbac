"""
-*- coding: utf-8 -*-
@File  : roles.py
@Author: 61ackPink
@Time : 2026/9/14 17:37
@Desc : 角色视图
"""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.serializers import RoleSerializer
from common.permissions import IsRootUser

from django.shortcuts import get_object_or_404


class RoleListCreateAPIView(GenericAPIView):
    """角色列表与创建接口"""

    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        根据请求方法使用不同的权限。

        GET：只要登录就可以查看角色
        POST：只有根管理员可以创建角色
        """
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsRootUser]

        # 权限类必须实例化后返回
        return [
            permission()
            for permission in permission_classes
        ]

    def get(self, request):
        """获取角色列表"""

        # Role 模型已经配置 ordering，
        # 所以查询结果默认按照 rank 从高到低排列
        roles = Role.objects.all()

        # many=True 表示序列化多个角色对象
        serializer = self.get_serializer(
            roles,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        """创建角色"""

        # 接收前端提交的数据
        serializer = self.get_serializer(
            data=request.data
        )

        # 验证名称、编码、权重等字段
        serializer.is_valid(raise_exception=True)

        # 调用 RoleSerializer 创建角色
        role = serializer.save()

        # 再序列化一次创建后的角色，
        # 返回 ID、创建时间等数据库生成的字段
        response_serializer = self.get_serializer(role)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

class RoleDetailAPIView(GenericAPIView):
    """单个角色的查询、修改和停用接口"""

    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        GET：登录用户可以查看角色详情

        PUT、PATCH、DELETE：
        只有根管理员可以修改或停用角色
        """

        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsRootUser]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_object(self):
        """
        获取当前路由对应的角色。

        路由中的 role_id 会被 Django 放入 self.kwargs。
        """

        role_id = self.kwargs["role_id"]

        return get_object_or_404(
            Role,
            id=role_id,
        )

    def get(self, request, *args, **kwargs):
        """获取角色详情"""

        role = self.get_object()

        serializer = self.get_serializer(role)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """完整修改角色"""

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        return Response(
            self.get_serializer(role).data
        )

    def patch(self, request, *args, **kwargs):
        """局部修改角色"""

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        role = serializer.save()

        return Response(
            self.get_serializer(role).data
        )

    def delete(self, request, *args, **kwargs):
        """停用角色"""

        role = self.get_object()

        role.is_active = False
        role.save(update_fields=["is_active"])

        return Response({
            "id": role.id,
            "name": role.name,
            "is_active": role.is_active,
            "message": "角色已停用",
        })