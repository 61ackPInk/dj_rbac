"""
-*- coding: utf-8 -*-
@File  : test_user_operation_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 10:38
@Desc : 用户管理操作权限隔离测试
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


class UserOperationPermissionTests(TestCase):
    """用户管理操作权限隔离测试"""

    def setUp(self):
        """创建每条测试需要的基础数据"""

        self.client = APIClient()

        # --------------------
        # 创建用户管理页面
        # --------------------

        self.users_page = Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            component="system/users/users.vue",
            icon="bi-people",
            sort_order=10,
            is_active=True,
        )

        # --------------------
        # 创建测试角色
        # --------------------

        self.operator_role = Role.objects.create(
            name="用户操作员",
            code="USER_OPERATOR",
            rank=500,
            description="测试用户管理权限",
            is_active=True,
        )

        self.target_role = Role.objects.create(
            name="普通员工",
            code="NORMAL_STAFF",
            rank=100,
            description="用于测试角色分配",
            is_active=True,
        )

        # 操作员必须先拥有用户管理页面
        self.users_page.visible_roles.add(
            self.operator_role,
        )

        # --------------------
        # 创建用户管理权限
        # --------------------

        permission_data = [
            (
                "查看用户列表",
                "USER_LIST",
                10,
            ),
            (
                "查看用户详情",
                "USER_DETAIL",
                20,
            ),
            (
                "创建用户",
                "USER_CREATE",
                30,
            ),
            (
                "修改用户资料",
                "USER_UPDATE",
                40,
            ),
            (
                "修改用户状态",
                "USER_CHANGE_STATUS",
                50,
            ),
            (
                "分配用户角色",
                "USER_ASSIGN_ROLE",
                60,
            ),
            (
                "重置用户密码",
                "USER_RESET_PASSWORD",
                70,
            ),
        ]

        self.permissions = {}

        for name, code, sort_order in permission_data:
            permission = Permission.objects.create(
                name=name,
                code=code,
                page=self.users_page,
                sort_order=sort_order,
                is_active=True,
            )

            self.permissions[code] = permission

        # --------------------
        # 创建操作员账号
        # --------------------

        self.operator = User.objects.create(
            username="user_operator",
            email="operator@example.com",
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

        # --------------------
        # 创建被管理用户
        # --------------------

        self.target_user = User.objects.create(
            username="target_user",
            email="target@example.com",
            is_active=True,
            is_root=False,
        )

        self.target_user.set_password(
            "TargetPassword123!"
        )

        self.target_user.save(
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
        """给操作员角色分配指定操作权限"""

        permissions = [
            self.permissions[code]
            for code in permission_codes
        ]

        self.operator_role.permissions.add(
            *permissions,
        )

    def test_user_list_does_not_allow_user_create(self):
        """
        只有 USER_LIST 时：

        可以查看用户列表；
        不能创建用户。
        """

        self.grant_permissions(
            "USER_LIST",
        )

        list_response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        create_response = self.client.post(
            "/api/users/",
            {
                "username": "created_user",
                "email": "created@example.com",
                "password": "CreatedPassword123!",
                "password_confirm": (
                    "CreatedPassword123!"
                ),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertFalse(
            User.objects.filter(
                username="created_user",
            ).exists()
        )

    def test_user_create_does_not_allow_user_list(self):
        """
        只有 USER_CREATE 时：

        可以创建用户；
        不能查看用户列表。
        """

        self.grant_permissions(
            "USER_CREATE",
        )

        create_response = self.client.post(
            "/api/users/",
            {
                "username": "created_user",
                "email": "created@example.com",
                "password": "CreatedPassword123!",
                "password_confirm": (
                    "CreatedPassword123!"
                ),
            },
            format="json",
        )

        self.assertEqual(
            create_response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                username="created_user",
            ).exists()
        )

        list_response = self.client.get(
            "/api/users/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_update_does_not_allow_status_change(
        self,
    ):
        """
        只有 USER_UPDATE 时：

        可以修改用户名和邮箱；
        不能停用用户。
        """

        self.grant_permissions(
            "USER_UPDATE",
        )

        update_response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/"
            ),
            {
                "username": "updated_target",
                "email": "updated@example.com",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_200_OK,
        )

        self.target_user.refresh_from_db()

        self.assertEqual(
            self.target_user.username,
            "updated_target",
        )

        status_response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/status/"
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

        self.target_user.refresh_from_db()

        self.assertTrue(
            self.target_user.is_active
        )

    def test_status_change_does_not_allow_user_update(
        self,
    ):
        """
        只有 USER_CHANGE_STATUS 时：

        可以停用用户；
        不能修改用户名和邮箱。
        """

        self.grant_permissions(
            "USER_CHANGE_STATUS",
        )

        update_response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/"
            ),
            {
                "username": "updated_target",
            },
            format="json",
        )

        self.assertEqual(
            update_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        status_response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/status/"
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

        self.target_user.refresh_from_db()

        self.assertFalse(
            self.target_user.is_active
        )

        self.assertEqual(
            self.target_user.username,
            "target_user",
        )

    def test_assign_role_permission_can_assign_role(self):
        """USER_ASSIGN_ROLE 可以给普通用户分配角色"""

        self.grant_permissions(
            "USER_ASSIGN_ROLE",
        )

        response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/role/"
            ),
            {
                "role_id": self.target_role.id,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.target_user.refresh_from_db()

        self.assertEqual(
            self.target_user.role_id,
            self.target_role.id,
        )

    def test_assign_role_permission_does_not_allow_update(
        self,
    ):
        """
        USER_ASSIGN_ROLE 只能分配角色，
        不能修改用户基本资料。
        """

        self.grant_permissions(
            "USER_ASSIGN_ROLE",
        )

        response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/"
            ),
            {
                "username": "updated_target",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.target_user.refresh_from_db()

        self.assertEqual(
            self.target_user.username,
            "target_user",
        )

    def test_reset_password_permission_can_reset_password(
        self,
    ):
        """USER_RESET_PASSWORD 可以重置普通用户密码"""

        self.grant_permissions(
            "USER_RESET_PASSWORD",
        )

        old_token_version = (
            self.target_user.token_version
        )

        response = self.client.patch(
            (
                f"/api/users/"
                f"{self.target_user.id}/password/"
            ),
            {
                "new_password": (
                    "NewSecurePassword456!"
                ),
                "new_password_confirm": (
                    "NewSecurePassword456!"
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.target_user.refresh_from_db()

        self.assertTrue(
            self.target_user.check_password(
                "NewSecurePassword456!"
            )
        )

        # 重置密码后 Token 版本必须递增，
        # 使该用户原来的 Token 全部失效
        self.assertEqual(
            self.target_user.token_version,
            old_token_version + 1,
        )