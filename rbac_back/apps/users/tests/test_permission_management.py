"""
-*- coding: utf-8 -*-
@File  : test_permission_management.py
@Author: 61ackPink
@Time : 2026/9/29 11:01
@Desc : 权限定义、角色授权和当前用户权限测试
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


class PermissionManagementTests(TestCase):
    """权限管理和当前用户权限测试"""

    def setUp(self):
        """创建权限管理测试数据"""

        self.client = APIClient()

        # --------------------
        # 创建测试页面
        # --------------------

        self.users_page = Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            sort_order=10,
            is_active=True,
        )

        self.hidden_page = Page.objects.create(
            name="隐藏页面",
            code="HIDDEN_PAGE",
            path="/hidden-page",
            sort_order=20,
            is_active=True,
        )

        # --------------------
        # 创建测试角色
        # --------------------

        self.role = Role.objects.create(
            name="系统管理员",
            code="SYSTEM_ADMIN",
            rank=500,
            is_active=True,
        )

        # --------------------
        # 创建操作权限
        # --------------------

        self.user_list_permission = (
            Permission.objects.create(
                name="查看用户列表",
                code="USER_LIST",
                page=self.users_page,
                sort_order=10,
                is_active=True,
            )
        )

        self.disabled_permission = (
            Permission.objects.create(
                name="修改用户资料",
                code="USER_UPDATE",
                page=self.users_page,
                sort_order=20,
                is_active=False,
            )
        )

        self.hidden_page_permission = (
            Permission.objects.create(
                name="查看隐藏页面",
                code="HIDDEN_PAGE_LIST",
                page=self.hidden_page,
                sort_order=10,
                is_active=True,
            )
        )

        # --------------------
        # 创建根管理员
        # --------------------

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

        # --------------------
        # 创建普通管理员
        # --------------------

        self.normal_user = User.objects.create(
            username="normal_admin",
            email="normal@example.com",
            role=self.role,
            is_active=True,
            is_root=False,
        )

        self.normal_user.set_password(
            "NormalPassword123!"
        )

        self.normal_user.save(
            update_fields=[
                "password",
            ]
        )

    def authenticate(self, user):
        """让客户端使用指定用户登录"""

        access_token = create_access_token(
            user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    def test_root_can_manage_permission_lifecycle(self):
        """
        根管理员可以查询、创建、修改和停用权限。
        """

        self.authenticate(
            self.root_user,
        )

        # 查询权限列表
        list_response = self.client.get(
            "/api/permissions/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        # 创建权限
        create_response = self.client.post(
            "/api/permissions/",
            {
                "name": "创建用户",
                "code": "USER_CREATE",
                "page_id": self.users_page.id,
                "description": "允许创建普通用户",
                "sort_order": 30,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        created_permission = (
            Permission.objects.get(
                code="USER_CREATE",
            )
        )

        # 修改权限
        update_response = self.client.patch(
            (
                f"/api/permissions/"
                f"{created_permission.id}/"
            ),
            {
                "description": (
                    "允许在用户管理中创建用户"
                ),
                "sort_order": 40,
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_200_OK,
        )

        created_permission.refresh_from_db()

        self.assertEqual(
            created_permission.sort_order,
            40,
        )

        # 停用权限
        disable_response = self.client.delete(
            (
                f"/api/permissions/"
                f"{created_permission.id}/"
            )
        )

        self.assertEqual(
            disable_response.status_code,
            status.HTTP_200_OK,
        )

        created_permission.refresh_from_db()

        self.assertFalse(
            created_permission.is_active
        )

    def test_non_root_cannot_manage_permissions(self):
        """
        普通用户不能管理权限定义，
        即使已经登录也不允许。
        """

        self.authenticate(
            self.normal_user,
        )

        list_response = self.client.get(
            "/api/permissions/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        create_response = self.client.post(
            "/api/permissions/",
            {
                "name": "创建用户",
                "code": "USER_CREATE",
                "page_id": self.users_page.id,
                "sort_order": 30,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            Permission.objects.filter(
                code="USER_CREATE",
            ).exists()
        )

    def test_root_can_assign_permissions_to_role(self):
        """
        根管理员可以给拥有对应页面的角色
        分配操作权限。
        """

        # 角色先拥有用户管理页面
        self.users_page.visible_roles.add(
            self.role,
        )

        self.authenticate(
            self.root_user,
        )

        response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.role.id}/permissions/"
            ),
            {
                "permission_ids": [
                    self.user_list_permission.id,
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.role.permissions.filter(
                id=self.user_list_permission.id,
            ).exists()
        )

    def test_permission_assignment_requires_page(self):
        """
        即使是根管理员，
        也不能把角色不可见页面中的权限
        分配给该角色。
        """

        self.authenticate(
            self.root_user,
        )

        # 当前 role 没有 hidden_page
        response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.role.id}/permissions/"
            ),
            {
                "permission_ids": [
                    self.hidden_page_permission.id,
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            self.role.permissions.filter(
                id=self.hidden_page_permission.id,
            ).exists()
        )

    def test_current_user_returns_only_effective_permissions(
        self,
    ):
        """
        /api/auth/me/ 只返回当前用户真正有效的权限。

        必须同时满足：
        1. 权限启用；
        2. 页面启用；
        3. 角色拥有页面；
        4. 角色拥有操作权限。
        """

        # 角色只拥有用户管理页面
        self.users_page.visible_roles.add(
            self.role,
        )

        # 人为加入三种权限关系：
        #
        # USER_LIST：有效；
        # USER_UPDATE：权限停用；
        # HIDDEN_PAGE_LIST：角色没有对应页面。
        self.role.permissions.add(
            self.user_list_permission,
            self.disabled_permission,
            self.hidden_page_permission,
        )

        self.authenticate(
            self.normal_user,
        )

        response = self.client.get(
            "/api/auth/me/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["permission_codes"],
            [
                "USER_LIST",
            ],
        )

    def test_root_current_user_returns_empty_permission_codes(
        self,
    ):
        """
        根管理员通过 is_root 直接放行，
        不需要返回数据库中的全部权限编码。
        """

        self.authenticate(
            self.root_user,
        )

        response = self.client.get(
            "/api/auth/me/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["is_root"]
        )

        self.assertEqual(
            response.data["permission_codes"],
            [],
        )