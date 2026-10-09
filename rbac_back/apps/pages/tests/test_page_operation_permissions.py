"""
-*- coding: utf-8 -*-
@File  : test_page_operation_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 10:56
@Desc : 页面管理操作权限隔离测试
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


class PageOperationPermissionTests(TestCase):
    """页面管理操作权限隔离测试"""

    def setUp(self):
        """创建页面权限测试需要的数据"""

        self.client = APIClient()

        # --------------------
        # 创建页面管理页面
        # --------------------

        self.pages_management_page = (
            Page.objects.create(
                name="页面管理",
                code="SYSTEM_PAGES",
                path="/system/pages",
                component=(
                    "system/pages/pages.vue"
                ),
                icon="bi-window-stack",
                sort_order=30,
                is_active=True,
            )
        )

        # --------------------
        # 创建被管理页面
        # --------------------

        self.target_page = Page.objects.create(
            name="测试页面",
            code="TEST_PAGE",
            path="/test-page",
            component="test/test-page.vue",
            icon="bi-file-earmark",
            sort_order=100,
            is_active=True,
        )

        # --------------------
        # 创建页面操作员角色
        # --------------------

        self.operator_role = Role.objects.create(
            name="页面操作员",
            code="PAGE_OPERATOR",
            rank=500,
            description="用于测试页面管理权限",
            is_active=True,
        )

        # 操作员必须先拥有页面管理页面
        self.pages_management_page.visible_roles.add(
            self.operator_role,
        )

        # 用于测试页面角色分配
        self.visible_role = Role.objects.create(
            name="页面访问角色",
            code="PAGE_VIEWER",
            rank=100,
            description="用于测试页面可见角色",
            is_active=True,
        )

        # --------------------
        # 创建页面管理操作权限
        # --------------------

        permission_data = [
            (
                "查看页面列表",
                "PAGE_LIST",
                10,
            ),
            (
                "查看页面详情",
                "PAGE_DETAIL",
                20,
            ),
            (
                "创建页面",
                "PAGE_CREATE",
                30,
            ),
            (
                "修改页面资料",
                "PAGE_UPDATE",
                40,
            ),
            (
                "修改页面状态",
                "PAGE_CHANGE_STATUS",
                50,
            ),
            (
                "分配页面角色",
                "PAGE_ASSIGN_ROLE",
                60,
            ),
        ]

        self.permissions = {}

        for name, code, sort_order in permission_data:
            permission = Permission.objects.create(
                name=name,
                code=code,
                page=self.pages_management_page,
                sort_order=sort_order,
                is_active=True,
            )

            self.permissions[code] = permission

        # --------------------
        # 创建页面操作员账号
        # --------------------

        self.operator = User.objects.create(
            username="page_operator",
            email="page_operator@example.com",
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
        """让测试客户端使用指定用户登录"""

        access_token = create_access_token(
            user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    def grant_permissions(self, *permission_codes):
        """给页面操作员分配指定权限"""

        permissions = [
            self.permissions[code]
            for code in permission_codes
        ]

        self.operator_role.permissions.add(
            *permissions,
        )

    def test_page_list_does_not_allow_page_create(self):
        """
        只有 PAGE_LIST 时：

        可以查看页面列表；
        不能创建页面。
        """

        self.grant_permissions(
            "PAGE_LIST",
        )

        list_response = self.client.get(
            "/api/pages/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        create_response = self.client.post(
            "/api/pages/",
            {
                "name": "新页面",
                "code": "NEW_PAGE",
                "path": "/new-page",
                "component": "new/new-page.vue",
                "icon": "bi-file-earmark-plus",
                "sort_order": 200,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            Page.objects.filter(
                code="NEW_PAGE",
            ).exists()
        )

    def test_page_create_does_not_allow_page_list(self):
        """
        只有 PAGE_CREATE 时：

        可以创建页面；
        不能查看页面列表。
        """

        self.grant_permissions(
            "PAGE_CREATE",
        )

        create_response = self.client.post(
            "/api/pages/",
            {
                "name": "新页面",
                "code": "NEW_PAGE",
                "path": "/new-page",
                "component": "new/new-page.vue",
                "icon": "bi-file-earmark-plus",
                "sort_order": 200,
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Page.objects.filter(
                code="NEW_PAGE",
            ).exists()
        )

        list_response = self.client.get(
            "/api/pages/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_page_detail_does_not_allow_page_update(
        self,
    ):
        """
        只有 PAGE_DETAIL 时：

        可以查看页面详情；
        不能修改页面资料。
        """

        self.grant_permissions(
            "PAGE_DETAIL",
        )

        detail_response = self.client.get(
            (
                f"/api/pages/"
                f"{self.target_page.id}/"
            )
        )

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

        update_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/"
            ),
            {
                "name": "修改后的页面",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.target_page.refresh_from_db()

        self.assertEqual(
            self.target_page.name,
            "测试页面",
        )

    def test_page_update_does_not_allow_status_change(
        self,
    ):
        """
        只有 PAGE_UPDATE 时：

        可以修改页面资料；
        不能停用页面。
        """

        self.grant_permissions(
            "PAGE_UPDATE",
        )

        update_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/"
            ),
            {
                "name": "修改后的页面",
                "sort_order": 150,
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_200_OK,
        )

        self.target_page.refresh_from_db()

        self.assertEqual(
            self.target_page.name,
            "修改后的页面",
        )

        status_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/status/"
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

        self.target_page.refresh_from_db()

        self.assertTrue(
            self.target_page.is_active
        )

    def test_status_change_does_not_allow_page_update(
        self,
    ):
        """
        只有 PAGE_CHANGE_STATUS 时：

        可以停用页面；
        不能修改页面资料。
        """

        self.grant_permissions(
            "PAGE_CHANGE_STATUS",
        )

        update_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/"
            ),
            {
                "name": "修改后的页面",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        status_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/status/"
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

        self.target_page.refresh_from_db()

        self.assertFalse(
            self.target_page.is_active
        )

        self.assertEqual(
            self.target_page.name,
            "测试页面",
        )

    def test_assign_role_permission_is_independent(
        self,
    ):
        """
        PAGE_ASSIGN_ROLE 可以给页面分配角色，
        但不能修改页面资料。
        """

        self.grant_permissions(
            "PAGE_ASSIGN_ROLE",
        )

        assign_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/roles/"
            ),
            {
                "role_ids": [
                    self.visible_role.id,
                ],
            },
            format="json",
        )

        self.assertEqual(
            assign_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.target_page.visible_roles.filter(
                id=self.visible_role.id,
            ).exists()
        )

        update_response = self.client.patch(
            (
                f"/api/pages/"
                f"{self.target_page.id}/"
            ),
            {
                "name": "修改后的页面",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.target_page.refresh_from_db()

        self.assertEqual(
            self.target_page.name,
            "测试页面",
        )