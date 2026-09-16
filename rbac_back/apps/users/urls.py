"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/9/10 16:58
@Desc : 用户功能API
"""
from django.urls import path

from apps.users.views import (
    # 用户
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    CurrentUserAPIView,
    RefreshTokenAPIView,
    UserPasswordChangeAPIView,
    # 角色
    RoleDetailAPIView,
    RoleListCreateAPIView,
    # 管理员操作用户
    UserListAPIView,
    UserRoleAssignAPIView,
    UserDetailAPIView,
    UserPasswordResetAPIView,
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
    # 退出登录
    path(
        "auth/logout/",
        UserLogoutAPIView.as_view(),
        name="user-logout",
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
    # 修改密码
    path(
        "auth/password/",
        UserPasswordChangeAPIView.as_view(),
        name="user-password-change",
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

    # --------------------
    # 管理员操作用户
    # --------------------

    # 用户列表
    path(
        "users/",
        UserListAPIView.as_view(),
        name="user-list",
    ),
    # 用户角色分配
    path(
        "users/<int:user_id>/role/",
        UserRoleAssignAPIView.as_view(),
        name="user-role-assign",
    ),
    # 用户详情、状态修改
    path(
        "users/<int:user_id>/",
        UserDetailAPIView.as_view(),
        name="user-detail",
    ),
    # 根管理员重置指定用户密码
    path(
        "users/<int:user_id>/password/",
        UserPasswordResetAPIView.as_view(),
        name="user-password-reset",
    ),

]
