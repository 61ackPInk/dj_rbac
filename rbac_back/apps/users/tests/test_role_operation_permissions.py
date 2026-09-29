"""
-*- coding: utf-8 -*-
@File  : test_role_operation_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 10:44
@Desc : 角色管理操作权限隔离测试
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


class RoleOperationPermissionTests(TestCase):
    """角色管理操作权限隔离测试"""

    def setUp(self):
        """创建角色权限测试所需的数据"""

        self.client = APIClient()

        # --------------------
        # 创建角色管理页面
        # --------------------

        self.roles_page = Page.objects.create(
            name="角色管理",
            code="SYSTEM_ROLES",
            path="/system/roles",
            component="system/roles/roles.vue",
            icon="bi-person-badge",
            sort_order=20,
            is_active=True,
        )

        # --------------------
        # 创建操作员角色
        # --------------------

        self.operator_role = Role.objects.create(
            name="角色操作员",
            code="ROLE_OPERATOR",
            rank=500,
            description="用于测试角色管理权限",
            is_active=True,
        )

        # 操作员必须拥有角色管理页面
        self.roles_page.visible_roles.add(
            self.operator_role,
        )

        # --------------------
        # 创建被管理角色
        # --------------------

        self.target_role = Role.objects.create(
            name="测试角色",
            code="TEST_ROLE",
            rank=200,
            description="被操作的测试角色",
            is_active=True,
        )

        # --------------------
        # 创建角色管理权限
        # --------------------

        permission_data = [
            (
                "查看角色列表",
                "ROLE_LIST",
                10,
            ),
            (
                "查看角色详情",
                "ROLE_DETAIL",
                20,
            ),
            (
                "创建角色",
                "ROLE_CREATE",
                30,
            ),
            (
                "修改角色资料",
                "ROLE_UPDATE",
                40,
            ),
            (
                "修改角色状态",
                "ROLE_CHANGE_STATUS",
                50,
            ),
        ]

        self.permissions = {}

        for name, code, sort_order in permission_data:
            permission = Permission.objects.create(
                name=name,
                code=code,
                page=self.roles_page,
                sort_order=sort_order,
                is_active=True,
            )

            self.permissions[code] = permission

        # --------------------
        # 创建操作员账号
        # --------------------

        self.operator = User.objects.create(
            username="role_operator",
            email="role_operator@example.com",
            role=self.operator_role,
            is_active=True,
            is_root=False,
        )

        self.operator.set_password(
            "OperatorPassword123!"
        )

        self.operator.save(
            update_fields=[
                "password",
            ]
        )

        self.authenticate(
            self.operator,
        )

    def authenticate(self, user):
        """让客户端使用指定用户的 Access Token"""

        access_token = create_access_token(
            user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    def grant_permissions(self, *permission_codes):
        """给操作员角色分配指定权限"""

        permissions = [
            self.permissions[code]
            for code in permission_codes
        ]

        self.operator_role.permissions.add(
            *permissions,
        )

    def test_role_list_does_not_allow_role_create(self):
        """
        只有 ROLE_LIST 时：

        可以查看角色列表；
        不能创建角色。
        """

        self.grant_permissions(
            "ROLE_LIST",
        )

        list_response = self.client.get(
            "/api/roles/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        create_response = self.client.post(
            "/api/roles/",
            {
                "name": "新角色",
                "code": "NEW_ROLE",
                "rank": 100,
                "description": "测试创建角色",
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            Role.objects.filter(
                code="NEW_ROLE",
            ).exists()
        )

    def test_role_create_does_not_allow_role_list(self):
        """
        只有 ROLE_CREATE 时：

        可以创建角色；
        不能查看角色列表。
        """

        self.grant_permissions(
            "ROLE_CREATE",
        )

        create_response = self.client.post(
            "/api/roles/",
            {
                "name": "新角色",
                "code": "NEW_ROLE",
                "rank": 100,
                "description": "测试创建角色",
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Role.objects.filter(
                code="NEW_ROLE",
            ).exists()
        )

        list_response = self.client.get(
            "/api/roles/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_role_detail_does_not_allow_role_update(self):
        """
        只有 ROLE_DETAIL 时：

        可以查看角色详情；
        不能修改角色资料。
        """

        self.grant_permissions(
            "ROLE_DETAIL",
        )

        detail_response = self.client.get(
            (
                f"/api/roles/"
                f"{self.target_role.id}/"
            )
        )

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

        update_response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/"
            ),
            {
                "name": "修改后的角色",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.target_role.refresh_from_db()

        self.assertEqual(
            self.target_role.name,
            "测试角色",
        )

    def test_role_update_does_not_allow_status_change(
        self,
    ):
        """
        只有 ROLE_UPDATE 时：

        可以修改角色资料；
        不能停用角色。
        """

        self.grant_permissions(
            "ROLE_UPDATE",
        )

        update_response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/"
            ),
            {
                "name": "修改后的角色",
                "description": "已经修改",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_200_OK,
        )

        self.target_role.refresh_from_db()

        self.assertEqual(
            self.target_role.name,
            "修改后的角色",
        )

        status_response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/status/"
            ),
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            status_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.target_role.refresh_from_db()

        self.assertTrue(
            self.target_role.is_active
        )

    def test_status_change_does_not_allow_role_update(
        self,
    ):
        """
        只有 ROLE_CHANGE_STATUS 时：

        可以停用角色；
        不能修改角色资料。
        """

        self.grant_permissions(
            "ROLE_CHANGE_STATUS",
        )

        update_response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/"
            ),
            {
                "name": "修改后的角色",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        status_response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/status/"
            ),
            {
                "is_active": False,
            },
            format="json",
        )

        self.assertEqual(
            status_response.status_code,
            status.HTTP_200_OK,
        )

        self.target_role.refresh_from_db()

        self.assertFalse(
            self.target_role.is_active
        )

        self.assertEqual(
            self.target_role.name,
            "测试角色",
        )

    def test_non_root_cannot_assign_role_permissions(self):
        """
        即使普通用户拥有全部角色管理权限，
        也不能给角色分配操作权限。

        角色权限分配接口仍然只允许根管理员。
        """

        self.grant_permissions(
            "ROLE_LIST",
            "ROLE_DETAIL",
            "ROLE_CREATE",
            "ROLE_UPDATE",
            "ROLE_CHANGE_STATUS",
        )

        response = self.client.patch(
            (
                f"/api/roles/"
                f"{self.target_role.id}/permissions/"
            ),
            {
                "permission_ids": [
                    self.permissions[
                        "ROLE_LIST"
                    ].id,
                ],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            self.target_role.permissions.exists()
        )