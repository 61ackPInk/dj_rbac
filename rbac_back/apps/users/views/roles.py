"""
-*- coding: utf-8 -*-
@File  : roles.py
@Author: 61ackPink
@Time : 2026/9/14 17:37
@Desc : 角色视图
"""
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.serializers import (
    RoleSerializer,
    RoleStatusUpdateSerializer,
)
from common.permissions import (
    HasOperationPermission,
)


class RoleListCreateAPIView(GenericAPIView):
    """
    角色列表与角色创建接口。

    GET：
        查询角色列表；
        需要 ROLE_LIST 权限。

    POST：
        创建一个新角色；
        需要 ROLE_CREATE 权限。
    """

    serializer_class = RoleSerializer

    # 使用操作权限校验，
    # 不再使用原来的 IsAuthenticated 或 IsRootUser
    permission_classes = [
        HasOperationPermission,
    ]

    # 同一个接口地址根据不同请求方法
    # 检查不同的操作权限
    required_permissions = {
        "GET": "ROLE_LIST",
        "POST": "ROLE_CREATE",
    }

    def get_queryset(self):
        """
        查询角色以及角色拥有的操作权限。

        RoleSerializer 会返回 permissions，
        而每一项 permission 又需要读取所属页面。

        使用 permissions__page 预加载后，
        可以避免序列化角色时反复查询数据库。
        """

        return Role.objects.prefetch_related(
            "permissions__page",
        )

    def get(self, request, *args, **kwargs):
        """获取全部角色"""

        roles = self.get_queryset()

        # many=True 表示当前序列化的是角色列表
        serializer = self.get_serializer(
            roles,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """创建一个新角色"""

        # 将前端提交的数据交给角色序列化器
        serializer = self.get_serializer(
            data=request.data,
        )

        # 验证角色名称、编码、权重等字段
        serializer.is_valid(
            raise_exception=True,
        )

        # 创建角色
        role = serializer.save()

        # 新角色创建后重新查询，
        # 确保响应中的 permissions 等关联字段完整
        role = self.get_queryset().get(
            id=role.id,
        )

        response_serializer = self.get_serializer(
            role,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class RoleDetailAPIView(GenericAPIView):
    """
    角色详情与角色资料修改接口。

    GET：
        查询指定角色详情；
        需要 ROLE_DETAIL 权限。

    PUT：
        完整修改角色资料；
        需要 ROLE_UPDATE 权限。

    PATCH：
        局部修改角色资料；
        需要 ROLE_UPDATE 权限。

    当前接口不能修改角色启用状态。
    启用和停用角色由 RoleStatusUpdateAPIView 处理。
    """

    serializer_class = RoleSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "ROLE_DETAIL",
        "PUT": "ROLE_UPDATE",
        "PATCH": "ROLE_UPDATE",
    }

    def get_queryset(self):
        """查询角色以及角色拥有的操作权限"""

        return Role.objects.prefetch_related(
            "permissions__page",
        )

    def get_object(self):
        """
        根据路由中的 role_id 查询角色。

        如果角色不存在，
        get_object_or_404() 会自动返回 404。
        """

        role_id = self.kwargs["role_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=role_id,
        )

    def get(self, request, *args, **kwargs):
        """查询指定角色详情"""

        role = self.get_object()

        serializer = self.get_serializer(
            role,
        )

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        完整修改指定角色资料。

        PUT 一般要求提交角色所有可修改字段：

        {
            "name": "系统管理员",
            "code": "SYSTEM_ADMIN",
            "rank": 900,
            "description": "负责系统管理"
        }

        is_active 是只读字段，
        不能通过当前接口修改。
        """

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        role = serializer.save()

        # 修改后重新查询关联权限，
        # 避免返回预加载缓存中的旧数据
        role = self.get_queryset().get(
            id=role.id,
        )

        response_serializer = self.get_serializer(
            role,
        )

        return Response(
            response_serializer.data,
        )

    def patch(self, request, *args, **kwargs):
        """
        局部修改指定角色资料。

        PATCH 只需要提交发生修改的字段，例如：

        {
            "name": "新的角色名称"
        }

        is_active 是只读字段，
        不能通过当前接口修改。
        """

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,

            # partial=True 表示允许只提交部分字段
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        role = serializer.save()

        # 修改后重新查询关联权限，
        # 确保响应数据是最新状态
        role = self.get_queryset().get(
            id=role.id,
        )

        response_serializer = self.get_serializer(
            role,
        )

        return Response(
            response_serializer.data,
        )


class RoleStatusUpdateAPIView(GenericAPIView):
    """
    角色启用状态修改接口。

    PATCH：
        启用或停用指定角色；
        需要 ROLE_CHANGE_STATUS 权限。
    """

    serializer_class = RoleStatusUpdateSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "PATCH": "ROLE_CHANGE_STATUS",
    }

    def get_queryset(self):
        """查询角色以及角色拥有的操作权限"""

        return Role.objects.prefetch_related(
            "permissions__page",
        )

    def get_object(self):
        """根据路由中的 role_id 查询角色"""

        role_id = self.kwargs["role_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=role_id,
        )

    def patch(self, request, *args, **kwargs):
        """
        修改指定角色的启用状态。

        停用角色：

        {
            "is_active": false
        }

        启用角色：

        {
            "is_active": true
        }
        """

        role = self.get_object()

        serializer = self.get_serializer(
            role,
            data=request.data,

            # 不使用 partial=True。
            #
            # RoleStatusUpdateSerializer 中的
            # is_active 是必填字段，
            # 因此请求必须明确提交状态。
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        role = serializer.save()

        # 状态修改后重新查询角色关联数据
        role = self.get_queryset().get(
            id=role.id,
        )

        response_serializer = RoleSerializer(
            role,
        )

        return Response(
            response_serializer.data,
        )