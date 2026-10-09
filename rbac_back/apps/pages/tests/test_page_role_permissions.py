"""
-*- coding: utf-8 -*-
@File  : test_page_role_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 10:28
@Desc : 页面角色与操作权限关系测试
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


class PageRolePermissionCleanupTests(TestCase):
    """页面取消角色后的权限清理测试"""

    def setUp(self):
        """创建测试需要的页面、角色和权限"""

        self.client = APIClient()

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

        self.role = Role.objects.create(
            name="用户管理员",
            code="USER_ADMIN",
            rank=500,
            is_active=True,
        )

        self.page = Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            sort_order=10,
            is_active=True,
        )

        self.list_permission = (
            Permission.objects.create(
                name="查看用户列表",
                code="USER_LIST",
                page=self.page,
                sort_order=10,
                is_active=True,
            )
        )

        self.update_permission = (
            Permission.objects.create(
                name="修改用户资料",
                code="USER_UPDATE",
                page=self.page,
                sort_order=20,
                is_active=True,
            )
        )

        # 页面和操作权限都分配给角色
        self.page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.list_permission,
            self.update_permission,
        )

        access_token = create_access_token(
            self.root_user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    def test_removing_role_from_page_removes_permissions(
        self,
    ):
        """
        页面取消角色后，
        删除该角色在当前页面下的全部操作权限。
        """

        response = self.client.patch(
            f"/api/pages/{self.page.id}/roles/",
            {
                "role_ids": [],
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertFalse(
            self.page.visible_roles.filter(
                id=self.role.id,
            ).exists()
        )

        self.assertFalse(
            self.role.permissions.filter(
                page=self.page,
            ).exists()
        )

    def test_reassigning_page_does_not_restore_permissions(
        self,
    ):
        """
        页面重新分配给角色后，
        原来的操作权限不能自动恢复。
        """

        # 第一次请求：移除角色
        remove_response = self.client.patch(
            f"/api/pages/{self.page.id}/roles/",
            {
                "role_ids": [],
            },
            format="json",
        )

        self.assertEqual(
            remove_response.status_code,
            status.HTTP_200_OK,
        )

        # 第二次请求：重新分配页面
        add_response = self.client.patch(
            f"/api/pages/{self.page.id}/roles/",
            {
                "role_ids": [
                    self.role.id,
                ],
            },
            format="json",
        )

        self.assertEqual(
            add_response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            self.page.visible_roles.filter(
                id=self.role.id,
            ).exists()
        )

        # 页面已经恢复，
        # 但操作权限必须由根管理员重新分配
        self.assertFalse(
            self.role.permissions.filter(
                page=self.page,
            ).exists()
        )