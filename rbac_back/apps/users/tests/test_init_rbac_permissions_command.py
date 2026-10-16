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
from common.permissions.registry import (
    load_permission_config,
)


class InitRbacPermissionsCommandTests(
    TestCase
):
    """RBAC 权限初始化命令测试"""

    # ==================== 动态权限配置 ====================

    def get_permission_config(self):
        """读取当前全部应用声明的权限配置。"""

        return load_permission_config()

    def get_expected_permission_codes(self):
        """返回当前配置中的全部权限编码。"""

        return {
            item["code"]
            for permission_items
            in self.get_permission_config().values()
            for item in permission_items
        }

    def create_required_pages(self):
        """根据当前权限配置动态创建所需页面。"""

        for index, page_code in enumerate(
            self.get_permission_config().keys(),
            start=1,
        ):
            Page.objects.create(
                name=f"测试页面-{page_code}",
                code=page_code,
                path=f"/test/page-{index}",
                sort_order=index * 10,
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
        """首次执行命令应创建全部已声明权限。"""

        self.create_required_pages()

        output = self.run_command()

        expected_codes = (
            self.get_expected_permission_codes()
        )
        expected_count = len(expected_codes)

        self.assertEqual(
            Permission.objects.count(),
            expected_count,
        )

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
            f"新建 {expected_count} 项",
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

        expected_count = len(
            self.get_expected_permission_codes()
        )

        # 第一次执行：创建权限
        self.run_command()

        self.assertEqual(
            Permission.objects.count(),
            expected_count,
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

        # 权限数量仍然是21，不会重复创建
        self.assertEqual(
            Permission.objects.count(),
            expected_count,
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
            f"更新 {expected_count} 项",
            output,
        )
