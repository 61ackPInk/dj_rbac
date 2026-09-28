"""
-*- coding: utf-8 -*-
@File  : __init__.py
@Author: 61ackPink
@Time : 2026/9/11 14:35
@Desc : 
"""
from .register import UserRegisterSerializer
from .login import UserLoginSerializer
from .refresh_token import RefreshTokenSerializer

from .users import (
    UserInfoSerializer,
    UserAdminUpdateSerializer,
    UserProfileUpdateSerializer,
    UserStatusUpdateSerializer,
)
from .roles import (
    RoleSerializer,
    RoleStatusUpdateSerializer,
)

from .user_roles import UserRoleAssignSerializer

from .passwords import (
    UserPasswordChangeSerializer,
    UserPasswordResetSerializer,
)

from .permissions import PermissionSerializer

from .role_permissions import (
    RolePermissionAssignSerializer,
)

__all__ = [
    "UserRegisterSerializer",
    "UserLoginSerializer",
    "RefreshTokenSerializer",
    "UserInfoSerializer",
    "UserAdminUpdateSerializer",
    "UserProfileUpdateSerializer",
    "UserStatusUpdateSerializer",
    "RoleSerializer",
    "RoleStatusUpdateSerializer",
    "UserRoleAssignSerializer",
    "UserPasswordChangeSerializer",
    "UserPasswordResetSerializer",
    "PermissionSerializer",
    "RolePermissionAssignSerializer",
]
