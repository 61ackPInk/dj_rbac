"""
-*- coding: utf-8 -*-
@File  : test_init_rbac_permissions_command.py
@Author: 61ackPink
@Time : 2026/9/29 11:12
@Desc : RBAC 权限初始化命令测试
"""
from io import StringIO

from django.core.management import (
    call_command,
)
from django.core.management.base import (
    CommandError,
)
from django.test import TestCase

from apps.pages.models import Page
from apps.users.models import Permission


class InitRbacPermissionsCommandTests(
    TestCase
):
    """RBAC 权限初始化命令测试"""

    def create_required_pages(self):
        """创建初始化权限所需的三个系统页面"""

        Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            sort_order=10,
            is_active=True,
        )

        Page.objects.create(
            name="角色管理",
            code="SYSTEM_ROLES",
            path="/system/roles",
            sort_order=20,
            is_active=True,
        )

        Page.objects.create(
            name="页面管理",
            code="SYSTEM_PAGES",
            path="/system/pages",
            sort_order=30,
            is_active=True,
        )

    def run_command(self):
        """执行初始化命令并接收输出"""

        output = StringIO()

        call_command(
            "init_rbac_permissions",
            stdout=output,
        )

        return output.getvalue()

    def test_missing_pages_raises_error_without_creating_permissions(
        self,
    ):
        """
        缺少系统页面时命令应报错，
        并且不能创建任何权限。
        """

        # 只创建用户管理页面，
        # 故意缺少角色管理和页面管理
        Page.objects.create(
            name="用户管理",
            code="SYSTEM_USERS",
            path="/system/users",
            sort_order=10,
            is_active=True,
        )

        with self.assertRaises(
            CommandError,
        ):
            self.run_command()

        self.assertEqual(
            Permission.objects.count(),
            0,
        )

    def test_command_creates_all_permissions(self):
        """首次执行命令应创建全部18项权限"""

        self.create_required_pages()

        output = self.run_command()

        self.assertEqual(
            Permission.objects.count(),
            18,
        )

        expected_codes = {
            # 用户管理
            "USER_LIST",
            "USER_DETAIL",
            "USER_CREATE",
            "USER_UPDATE",
            "USER_CHANGE_STATUS",
            "USER_ASSIGN_ROLE",
            "USER_RESET_PASSWORD",

            # 角色管理
            "ROLE_LIST",
            "ROLE_DETAIL",
            "ROLE_CREATE",
            "ROLE_UPDATE",
            "ROLE_CHANGE_STATUS",

            # 页面管理
            "PAGE_LIST",
            "PAGE_DETAIL",
            "PAGE_CREATE",
            "PAGE_UPDATE",
            "PAGE_CHANGE_STATUS",
            "PAGE_ASSIGN_ROLE",
        }

        actual_codes = set(
            Permission.objects.values_list(
                "code",
                flat=True,
            )
        )

        self.assertEqual(
            actual_codes,
            expected_codes,
        )

        self.assertIn(
            "新建 18 项",
            output,
        )

    def test_command_is_idempotent_and_updates_permissions(
        self,
    ):
        """
        重复执行命令不会创建重复数据，
        并会恢复内置权限的标准配置。
        """

        self.create_required_pages()

        # 第一次执行：创建权限
        self.run_command()

        self.assertEqual(
            Permission.objects.count(),
            18,
        )

        # 人为修改一条内置权限
        permission = Permission.objects.get(
            code="USER_LIST",
        )

        permission.name = "错误名称"
        permission.description = "错误描述"
        permission.sort_order = 999
        permission.is_active = False

        permission.save(
            update_fields=[
                "name",
                "description",
                "sort_order",
                "is_active",
            ]
        )

        # 第二次执行：更新现有权限
        output = self.run_command()

        # 权限数量仍然是18，不会重复创建
        self.assertEqual(
            Permission.objects.count(),
            18,
        )

        permission.refresh_from_db()

        self.assertEqual(
            permission.name,
            "查看用户列表",
        )

        self.assertEqual(
            permission.description,
            "允许查看系统用户列表",
        )

        self.assertEqual(
            permission.sort_order,
            10,
        )

        self.assertTrue(
            permission.is_active
        )

        self.assertIn(
            "新建 0 项",
            output,
        )

        self.assertIn(
            "更新 18 项",
            output,
        )