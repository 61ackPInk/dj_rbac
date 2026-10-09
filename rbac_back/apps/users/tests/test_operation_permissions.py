"""
-*- coding: utf-8 -*-
@File  : test_operation_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 10:00
@Desc : 操作权限核心规则测试
"""
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from apps.pages.models import Page
from apps.users.models import (
    Permission,
    Role,
    User,
)
from common.utils.jwt import create_access_token


class OperationPermissionTests(TestCase):
    """操作权限核心规则测试"""

    def setUp(self):
        """为每条测试创建独立的基础数据"""

        self.client = APIClient()

        # 创建用户管理页面
        self.users_page = Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            component="system/users/users.vue",
            icon="bi-people",
            sort_order=10,
            is_active=True,
        )

        # 创建普通管理员角色
        self.role = Role.objects.create(
            name="用户管理员",
            code="USER_ADMIN",
            rank=500,
            description="负责管理系统用户",
            is_active=True,
        )

        # 创建查看用户列表权限
        self.user_list_permission = (
            Permission.objects.create(
                name="查看用户列表",
                code="USER_LIST",
                page=self.users_page,
                description="允许查看系统用户列表",
                sort_order=10,
                is_active=True,
            )
        )

        # 创建普通用户
        self.user = User.objects.create(
            username="normal_admin",
            email="normal@example.com",
            role=self.role,
            is_active=True,
            is_root=False,
        )

        self.user.set_password(
            "TestPassword123!"
        )
        self.user.save(
            update_fields=[
                "password",
            ]
        )

        # 创建根管理员
        self.root_user = User.objects.create(
            username="root_admin",
            email="root@example.com",
            is_active=True,
            is_root=True,
        )

        self.root_user.set_password(
            "RootPassword123!"
        )
        self.root_user.save(
            update_fields=[
                "password",
            ]
        )

    def authenticate(self, user):
        """让测试客户端携带指定用户的 Access Token"""

        access_token = create_access_token(
            user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    def test_root_user_can_access_without_role(self):
        """
        根管理员没有角色和操作权限时，
        仍然可以访问受保护接口。
        """

        self.authenticate(
            self.root_user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_with_page_and_permission_can_access(self):
        """
        普通用户同时拥有页面和操作权限时，
        可以访问对应接口。
        """

        # 把用户管理页面分配给该角色
        self.users_page.visible_roles.add(
            self.role,
        )

        # 把 USER_LIST 权限分配给该角色
        self.role.permissions.add(
            self.user_list_permission,
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_with_page_but_without_permission_is_denied(
        self,
    ):
        """
        角色拥有页面但没有 USER_LIST 时，
        不能查看用户列表。
        """

        self.users_page.visible_roles.add(
            self.role,
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_with_permission_but_without_page_is_denied(
        self,
    ):
        """
        角色拥有 USER_LIST，但没有用户管理页面时，
        仍然不能查看用户列表。
        """

        # 直接制造一条不完整权限关系，
        # 用于验证后端权限类的双重保护
        self.role.permissions.add(
            self.user_list_permission,
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_without_role_is_denied(self):
        """没有角色的普通用户不能访问管理接口"""

        self.user.role = None
        self.user.save(
            update_fields=[
                "role",
            ]
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_disabled_role_is_denied(self):
        """角色停用后不能继续使用操作权限"""

        self.users_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.user_list_permission,
        )

        self.role.is_active = False
        self.role.save(
            update_fields=[
                "is_active",
            ]
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_disabled_page_is_denied(self):
        """权限所属页面停用后不能继续访问接口"""

        self.users_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.user_list_permission,
        )

        self.users_page.is_active = False
        self.users_page.save(
            update_fields=[
                "is_active",
            ]
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_disabled_permission_is_denied(self):
        """操作权限停用后不能继续访问接口"""

        self.users_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.user_list_permission,
        )

        self.user_list_permission.is_active = False
        self.user_list_permission.save(
            update_fields=[
                "is_active",
            ]
        )

        self.authenticate(
            self.user,
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_disabled_user_is_denied(self):
        """账号停用后原来的 Token 不能继续使用"""

        self.users_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.user_list_permission,
        )

        # 先签发 Token，
        # 再停用用户账号
        self.authenticate(
            self.user,
        )

        self.user.is_active = False
        self.user.save(
            update_fields=[
                "is_active",
            ]
        )

        response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )