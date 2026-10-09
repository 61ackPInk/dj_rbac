"""
-*- coding: utf-8 -*-
@File  : pages.py
@Author: 61ackPink
@Time : 2026/9/16 16:05
@Desc :
"""
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.pages.models import Page
from apps.pages.serializers import (
    PageRoleAssignSerializer,
    PageSerializer,
    PageStatusUpdateSerializer,
    VisiblePageSerializer,
)
from common.permissions import (
    HasOperationPermission,
)


class PageListCreateAPIView(GenericAPIView):
    """
    页面列表和页面创建接口。

    GET：
        查询全部页面；
        需要 PAGE_LIST 权限。

    POST：
        创建新页面；
        需要 PAGE_CREATE 权限。
    """

    serializer_class = PageSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PAGE_LIST",
        "POST": "PAGE_CREATE",
    }

    def get_queryset(self):
        """
        查询页面及关联数据。

        select_related("parent")：
            一次性查询父页面。

        prefetch_related("visible_roles")：
            一次性查询页面可见角色。
        """

        return Page.objects.select_related(
            "parent",
        ).prefetch_related(
            "visible_roles",
        )

    def get(self, request, *args, **kwargs):
        """查询全部页面，包括停用页面"""

        pages = self.get_queryset()

        serializer = self.get_serializer(
            pages,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        创建页面。

        当前接口只创建页面基本信息，
        不负责给页面分配角色。

        页面创建完成后，需要调用：
        PATCH /api/pages/{id}/roles/
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        page = serializer.save()

        page = self.get_queryset().get(
            id=page.id,
        )

        response_serializer = self.get_serializer(
            page,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PageDetailAPIView(GenericAPIView):
    """
    页面详情和页面资料修改接口。

    GET：
        查询页面详情；
        需要 PAGE_DETAIL 权限。

    PATCH：
        修改页面资料；
        需要 PAGE_UPDATE 权限。

    当前接口不能修改：
        is_active
        visible_roles
    """

    serializer_class = PageSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PAGE_DETAIL",
        "PATCH": "PAGE_UPDATE",
    }

    def get_queryset(self):
        """查询页面及关联数据"""

        return Page.objects.select_related(
            "parent",
        ).prefetch_related(
            "visible_roles",
        )

    def get_object(self):
        """根据 page_id 查询页面"""

        page_id = self.kwargs["page_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=page_id,
        )

    def get(self, request, *args, **kwargs):
        """查询指定页面详情"""

        page = self.get_object()

        serializer = self.get_serializer(
            page,
        )

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        局部修改页面基本信息。

        可以修改：
            name
            code
            path
            component
            icon
            parent_id
            sort_order

        不能修改：
            is_active
            visible_roles
        """

        page = self.get_object()

        serializer = self.get_serializer(
            page,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        page = serializer.save()

        page = self.get_queryset().get(
            id=page.id,
        )

        response_serializer = self.get_serializer(
            page,
        )

        return Response(
            response_serializer.data,
        )


class PageStatusUpdateAPIView(GenericAPIView):
    """
    页面启用状态修改接口。

    PATCH：
        启用或停用页面；
        需要 PAGE_CHANGE_STATUS 权限。
    """

    serializer_class = PageStatusUpdateSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "PATCH": "PAGE_CHANGE_STATUS",
    }

    def get_queryset(self):
        """查询页面及关联数据"""

        return Page.objects.select_related(
            "parent",
        ).prefetch_related(
            "visible_roles",
        )

    def get_object(self):
        """根据 page_id 查询页面"""

        page_id = self.kwargs["page_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=page_id,
        )

    def patch(self, request, *args, **kwargs):
        """
        修改页面启用状态。

        停用：

        {
            "is_active": false
        }

        启用：

        {
            "is_active": true
        }
        """

        page = self.get_object()

        serializer = self.get_serializer(
            page,
            data=request.data,

            # is_active 必须提交
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        page = serializer.save()

        page = self.get_queryset().get(
            id=page.id,
        )

        response_serializer = PageSerializer(
            page,
        )

        return Response(
            response_serializer.data,
        )


class PageRoleAssignAPIView(GenericAPIView):
    """
    页面可见角色分配接口。

    GET：
        查询页面当前分配的角色；
        需要 PAGE_DETAIL 权限。

    PATCH：
        替换页面的全部可见角色；
        需要 PAGE_ASSIGN_ROLE 权限。
    """

    serializer_class = PageRoleAssignSerializer

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PAGE_DETAIL",
        "PATCH": "PAGE_ASSIGN_ROLE",
    }

    def get_queryset(self):
        """查询页面及可见角色"""

        return Page.objects.select_related(
            "parent",
        ).prefetch_related(
            "visible_roles",
        )

    def get_object(self):
        """根据 page_id 查询页面"""

        page_id = self.kwargs["page_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=page_id,
        )

    def get(self, request, *args, **kwargs):
        """查询页面当前的可见角色"""

        page = self.get_object()

        response_serializer = PageSerializer(
            page,
        )

        return Response(
            response_serializer.data,
        )

    def patch(self, request, *args, **kwargs):
        """替换页面的全部可见角色"""

        page = self.get_object()

        serializer = self.get_serializer(
            page,
            data=request.data,

            # role_ids 必须提交
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        page = serializer.save()

        # 多对多关系修改后重新查询，
        # 避免返回预加载缓存中的旧角色数据
        page = self.get_queryset().get(
            id=page.id,
        )

        response_serializer = PageSerializer(
            page,
        )

        return Response(
            response_serializer.data,
        )


class VisiblePageListAPIView(GenericAPIView):
    """
    当前用户可见页面接口。

    该接口用于前端生成菜单，
    只要求用户已经登录。

    页面过滤逻辑仍然按照：
        根管理员查看全部启用页面；
        普通用户查看角色被分配的启用页面。
    """

    serializer_class = VisiblePageSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        """根据当前用户过滤可见页面"""

        user = self.request.user

        # 只查询启用状态的页面
        pages = Page.objects.filter(
            is_active=True,
        )

        # 根管理员查看全部启用页面
        if user.is_root:
            return pages

        # 普通用户没有角色时返回空列表
        if user.role_id is None:
            return pages.none()

        # 用户角色停用后返回空列表
        if not user.role.is_active:
            return pages.none()

        # 只返回明确分配给当前角色的页面
        return pages.filter(
            visible_roles__id=user.role_id,
        ).distinct()

    def get(self, request, *args, **kwargs):
        """返回当前用户可见页面"""

        pages = self.get_queryset()

        serializer = self.get_serializer(
            pages,
            many=True,
        )

        return Response(serializer.data)