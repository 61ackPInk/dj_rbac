"""
-*- coding: utf-8 -*-
@File  : __init__.py
@Author: 61ackPink
@Time : 2026/9/11 14:44
@Desc : 
"""
from .register import UserRegisterAPIView
from .login import UserLoginAPIView
from .current_user import CurrentUserAPIView
from .refresh_token import RefreshTokenAPIView
from .roles import (
    RoleListCreateAPIView,
    RoleDetailAPIView
)
from .user_roles import UserRoleAssignAPIView
from .users import (
    UserListAPIView,
    UserDetailAPIView,
)

__all__ = [
    "UserRegisterAPIView",
    "UserLoginAPIView",
    "CurrentUserAPIView",
    "RefreshTokenAPIView",
    "RoleListCreateAPIView",
    "RoleDetailAPIView",
    "UserRoleAssignAPIView",
    "UserListAPIView",
    "UserDetailAPIView"
]
