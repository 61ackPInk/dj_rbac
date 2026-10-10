"""
-*- coding: utf-8 -*-
@File  : system_dashboaro.py.py
@Author: 61ackPink
@Time : 2026/10/9 18:28
@Desc : 
"""
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.pages.models import Page
from apps.users.models import Role, User
from common.permissions.pages import CanAccessPage


class SystemOverviewAPIView(GenericAPIView):
    """系统概览：返回用户、角色、页面的基础统计。"""

    # 访问统计接口前，先检查是否有权查看“系统概览”页面
    permission_classes = [CanAccessPage]
    required_page_code = "SYSTEM_DASHBOARD"

    def get(self, request, *args, **kwargs):
        # total 包含启用和停用的数据；active 只统计启用的数据
        data = {
            "users": {
                "total": User.objects.count(),
                "active": User.objects.filter(is_active=True).count(),
            },
            "roles": {
                "total": Role.objects.count(),
                "active": Role.objects.filter(is_active=True).count(),
            },
            "pages": {
                "total": Page.objects.count(),
                "active": Page.objects.filter(is_active=True).count(),
            },
        }

        # 项目的自定义 JSON Renderer 会负责包装 code/message/data
        return Response(data)