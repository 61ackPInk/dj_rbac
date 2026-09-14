"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/9/10 16:58
@Desc : 用户功能API
"""
from django.urls import path

from apps.users.views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    CurrentUserAPIView,
    RefreshTokenAPIView,
    RoleListCreateAPIView,
)

# 接口
urlpatterns = [
    # 用户注册
    path(
        "auth/register/",
        UserRegisterAPIView.as_view(),
        name="user-register",
    ),
    # 用户登录
    path(
        "auth/login/",
        UserLoginAPIView.as_view(),
        name="user-login",
    ),
    # 用户信息
    path(
        "auth/me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),
    # 刷新Token
    path(
        "auth/refresh/",
        RefreshTokenAPIView.as_view(),
        name="refresh-token",
    ),

    # --------------------
    # 角色管理
    # --------------------

    path(
        "roles/",
        RoleListCreateAPIView.as_view(),
        name="role-list-create",
    ),
]