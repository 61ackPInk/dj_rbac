"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/14 17:28
@Desc : 
"""
from rest_framework.permissions import BasePermission


class IsRootUser(BasePermission):
    """只允许根管理员访问"""

    # 权限验证失败时，DRF 返回的提示
    message = "只有根管理员才能执行此操作"

    def has_permission(self, request, view):
        """
        判断当前请求是否拥有访问权限。

        返回 True：允许继续执行视图
        返回 False：拒绝访问，通常返回 403
        """

        # JWTAuthentication 验证成功后，
        # 当前用户对象会被放在 request.user 中
        user = request.user

        # getattr() 可以避免 user 没有对应属性时直接报错
        is_authenticated = getattr(
            user,
            "is_authenticated",
            False,
        )

        is_active = getattr(
            user,
            "is_active",
            False,
        )

        is_root = getattr(
            user,
            "is_root",
            False,
        )

        # 必须同时满足：
        # 1. 用户已经登录
        # 2. 用户账号处于启用状态
        # 3. 用户是根管理员
        return bool(
            is_authenticated
            and is_active
            and is_root
        )