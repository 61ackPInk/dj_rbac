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
    RoleDetailAPIView,
    RoleListCreateAPIView,
    UserRoleAssignAPIView
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

    # POST：创建  GET：角色列表查询
    path(
        "roles/",
        RoleListCreateAPIView.as_view(),
        name="role-list-create",
    ),
    # GET：查询单个, PUT、PATCH、DELETE
    path(
        "roles/<int:role_id>/",
        RoleDetailAPIView.as_view(),
        name="role-detail",
    ),
    # 给用户分配或取消角色
    path(
        "users/<int:user_id>/role/",
        UserRoleAssignAPIView.as_view(),
        name="user-role-assign",
    ),
]