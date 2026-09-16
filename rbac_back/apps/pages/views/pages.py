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
from rest_framework.response import Response

from apps.pages.models import Page
from apps.pages.serializers import PageSerializer
from common.permissions import IsRootUser

from rest_framework.permissions import IsAuthenticated

from apps.pages.serializers import (
    PageSerializer,
    VisiblePageSerializer,
)


class PageListCreateAPIView(GenericAPIView):
    """根管理员查询和创建页面"""

    serializer_class = PageSerializer
    permission_classes = [IsRootUser]

    def get_queryset(self):
        """
        提前读取父页面和可见角色，
        避免序列化每个页面时重复查询数据库。
        """

        return Page.objects.select_related(
            "parent"
        ).prefetch_related(
            "visible_roles"
        )

    def get(self, request, *args, **kwargs):
        """查询全部页面，包括已停用页面"""

        pages = self.get_queryset()

        serializer = self.get_serializer(
            pages,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """创建页面并配置可见角色"""

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        # ModelSerializer 会自动保存页面，
        # 并处理 visible_roles 多对多关系
        page = serializer.save()

        # 重新查询，提前加载响应所需的关联数据
        page = self.get_queryset().get(id=page.id)

        response_serializer = self.get_serializer(page)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PageDetailAPIView(GenericAPIView):
    """根管理员查询、修改和停用指定页面"""

    serializer_class = PageSerializer
    permission_classes = [IsRootUser]

    def get_queryset(self):
        """读取页面以及关联信息"""

        return Page.objects.select_related(
            "parent"
        ).prefetch_related(
            "visible_roles"
        )

    def get_object(self):
        """根据路由中的 page_id 查询页面"""

        page_id = self.kwargs["page_id"]

        return get_object_or_404(
            self.get_queryset(),
            id=page_id,
        )

    def get(self, request, *args, **kwargs):
        """查询页面详情"""

        page = self.get_object()

        serializer = self.get_serializer(page)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """局部修改页面，包括父页面和可见角色"""

        page = self.get_object()

        serializer = self.get_serializer(
            page,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        page = serializer.save()

        # 修改多对多关系后重新查询，
        # 避免使用之前预加载的旧角色数据
        page = self.get_queryset().get(id=page.id)

        response_serializer = self.get_serializer(page)

        return Response(response_serializer.data)

    def delete(self, request, *args, **kwargs):
        """停用页面，不真正删除数据库记录"""

        page = self.get_object()
        page.is_active = False

        # 同时更新 update_time，
        # 因为指定 update_fields 时 auto_now 字段
        # 只有被包含在其中才会更新
        page.save(
            update_fields=[
                "is_active",
                "update_time",
            ]
        )

        return Response({
            "id": page.id,
            "name": page.name,
            "is_active": page.is_active,
            "message": "页面已停用",
        })


class VisiblePageListAPIView(GenericAPIView):
    """获取当前用户可以查看的页面"""

    serializer_class = VisiblePageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """根据当前用户身份过滤页面"""

        user = self.request.user

        # 只查询已启用页面
        pages = Page.objects.filter(
            is_active=True
        )

        # 根管理员不受普通角色分配限制
        if user.is_root:
            return pages

        # 没有角色时必须返回空列表。
        #
        # 不能直接使用 visible_roles=None 查询，
        # 否则可能查到没有分配任何角色的页面。
        if user.role_id is None:
            return pages.none()

        # 角色停用后，该角色用户不能再查看分配的页面
        if not user.role.is_active:
            return pages.none()

        # 只查询明确分配给当前角色的页面
        return pages.filter(
            visible_roles__id=user.role_id
        ).distinct()

    def get(self, request, *args, **kwargs):
        """返回当前用户可见页面列表"""

        pages = self.get_queryset()

        serializer = self.get_serializer(
            pages,
            many=True,
        )

        return Response(serializer.data)

