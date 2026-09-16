"""
-*- coding: utf-8 -*-
@File  : pages.py
@Author: 61ackPink
@Time : 2026/9/16 18:24
@Desc : 页面权限
"""
from rest_framework.permissions import BasePermission

from apps.pages.models import Page


class CanAccessPage(BasePermission):
    """检查当前用户是否拥有指定页面的访问权限"""

    message = "你没有访问该页面的权限"

    def has_permission(self, request, view):
        """在执行业务视图前检查页面授权"""

        user = request.user

        # 未登录或账号已停用，不允许访问
        if not getattr(user, "is_authenticated", False):
            return False

        if not getattr(user, "is_active", False):
            return False

        # 业务视图必须明确声明需要哪个页面的权限
        page_code = getattr(
            view,
            "required_page_code",
            None,
        )

        # 未配置页面编码时拒绝访问，
        # 避免开发时遗漏配置造成权限绕过
        if not page_code:
            return False

        # 页面必须存在且处于启用状态
        pages = Page.objects.filter(
            code=page_code,
            is_active=True,
        )

        # 根管理员绕过角色分配检查，
        # 但仍不能访问不存在或已停用的页面
        if user.is_root:
            return pages.exists()

        # 普通用户必须拥有一个有效角色
        if user.role_id is None:
            return False

        if not user.role.is_active:
            return False

        # 页面必须明确分配给当前角色
        return pages.filter(
            visible_roles__id=user.role_id
        ).exists()