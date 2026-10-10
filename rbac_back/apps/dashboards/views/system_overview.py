"""
-*- coding: utf-8 -*-
@File  : system_overview.py.py
@Author: 61ackPink
@Time : 2026/10/9 18:28
@Desc : 
"""
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

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
        # 以当前时间往前推 7 天，作为“新增用户”的起点
        new_user_start = timezone.now() - timedelta(days=7)

        # 三类互不重叠：启用且较早注册、启用且最近注册、已禁用
        normal_users = User.objects.filter(
            is_active=True,
            create_time__lt=new_user_start,
        ).count()

        new_users = User.objects.filter(
            is_active=True,
            create_time__gte=new_user_start,
        ).count()

        disabled_users = User.objects.filter(
            is_active=False,
        ).count()

        # users 是 User.role 设置的 related_name。
        # annotate 会让数据库按角色统计用户数，避免逐个角色查询。
        role_distribution = list(
            Role.objects.annotate(
                user_count=Count("users"),
            ).values(
                "id",
                "name",
                "code",
                "user_count",
            )
        )

        # 新注册用户可能尚未分配角色，单独统计这一部分
        unassigned_user_count = User.objects.filter(
            role__isnull=True,
        ).count()

        # 同时取出用户关联的角色，避免展示 5 个用户时再查询 5 次角色
        latest_users = User.objects.select_related("role").order_by(
            "-create_time",
            "-id",  # 注册时间相同时，用 ID 保证顺序稳定
        )[:5]

        recent_users = [
            {
                "id": user.id,
                "username": user.username,
                "role": user.role.name if user.role else "未分配角色",
                "status": "启用" if user.is_active else "已禁用",
            }
            for user in latest_users
        ]

        # total 包含启用和停用的数据；active 只统计启用的数据
        data = {
            # 用户数据
            "users": {
                "total": User.objects.count(),
                "active": User.objects.filter(is_active=True).count(),
                "status": {
                    "normal": normal_users,  # 正常用户
                    "new": new_users,  # 新用户
                    "disabled": disabled_users,  # 已禁用
                },
            },
            # 角色数据
            "roles": {
                "total": Role.objects.count(),
                "active": Role.objects.filter(is_active=True).count(),
            },
            # 页面数据
            "pages": {
                # 系统中全部页面，包含启用和禁用
                "total": Page.objects.count(),

                # 当前启用的页面
                "active": Page.objects.filter(is_active=True).count(),

                # 没有父页面的页面，即一级页面
                "top_level": Page.objects.filter(parent__isnull=True).count(),

                # 当前禁用的页面
                "disabled": Page.objects.filter(is_active=False).count(),
            },
            # 角色分布
            "role_distribution": {
                "items": role_distribution,
                "unassigned_user_count": unassigned_user_count,
            },
            # 最近新增用户
            "recent_users": recent_users,
        }

        # 项目的自定义 JSON Renderer 会负责包装 code/message/data
        return Response(data)
