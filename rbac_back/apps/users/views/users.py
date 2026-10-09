"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/15 15:31
@Desc : 用户视图
"""
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import (
    UserAdminUpdateSerializer,
    UserInfoSerializer,
    UserRegisterSerializer,
    UserStatusUpdateSerializer,
)
from common.permissions import (
    HasOperationPermission,
)


class UserListAPIView(GenericAPIView):
    """用户列表和管理员创建用户接口"""

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "USER_LIST",
        "POST": "USER_CREATE",
    }

    def get_serializer_class(self):
        """根据请求方法选择序列化器"""

        if self.request.method == "POST":
            return UserRegisterSerializer

        return UserInfoSerializer

    def get(self, request, *args, **kwargs):
        """获取全部用户及其角色"""

        users = User.objects.select_related(
            "role",
        ).order_by(
            "id",
        )

        serializer = self.get_serializer(
            users,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        管理员创建普通用户。

        创建结果不会成为根管理员，
        角色需要通过角色分配接口单独设置。
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        user = User.objects.select_related(
            "role",
        ).get(
            id=user.id,
        )

        response_serializer = UserInfoSerializer(
            user,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserDetailAPIView(GenericAPIView):
    """用户详情和用户资料修改接口"""

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "USER_DETAIL",
        "PATCH": "USER_UPDATE",
    }

    def get_serializer_class(self):
        """根据请求方法选择序列化器"""

        if self.request.method == "GET":
            return UserInfoSerializer

        return UserAdminUpdateSerializer

    def get_object(self):
        """根据 user_id 查询用户"""

        user_id = self.kwargs["user_id"]

        return get_object_or_404(
            User.objects.select_related(
                "role",
            ),
            id=user_id,
        )

    def get(self, request, *args, **kwargs):
        """获取指定用户详情"""

        user = self.get_object()

        serializer = self.get_serializer(
            user,
        )

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """修改指定用户的用户名或邮箱"""

        user = self.get_object()

        # 普通权限管理员不能修改根管理员资料
        if (
            user.is_root
            and not request.user.is_root
        ):
            raise PermissionDenied(
                "不能修改根管理员资料"
            )

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        user = User.objects.select_related(
            "role",
        ).get(
            id=user.id,
        )

        return Response(
            UserInfoSerializer(user).data,
        )


class UserStatusUpdateAPIView(GenericAPIView):
    """修改指定用户的启用状态"""

    serializer_class = UserStatusUpdateSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "PATCH": "USER_CHANGE_STATUS",
    }

    def get_object(self):
        """根据 user_id 查询用户"""

        user_id = self.kwargs["user_id"]

        return get_object_or_404(
            User.objects.select_related(
                "role",
            ),
            id=user_id,
        )

    def patch(self, request, *args, **kwargs):
        """启用或停用指定用户"""

        user = self.get_object()

        # 非根管理员不能修改根管理员状态
        if (
            user.is_root
            and not request.user.is_root
        ):
            raise PermissionDenied(
                "不能修改根管理员状态"
            )

        serializer = self.get_serializer(
            user,
            data=request.data,

            # is_active 必须提交，所以不使用 partial=True
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.save()

        return Response(
            UserInfoSerializer(user).data,
        )

