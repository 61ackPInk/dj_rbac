"""
-*- coding: utf-8 -*-
@File  : init_rbac_permissions.py
@Author: 61ackPink
@Time : 2026/9/29 11:05
@Desc : 初始化 RBAC 系统操作权限

python.exe manage.py init_rbac_permissions
"""
from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import transaction

from apps.pages.models import Page
from apps.users.models import Permission


class Command(BaseCommand):
    """初始化系统内置操作权限"""

    help = (
        "根据系统页面创建或更新 RBAC 操作权限"
    )

    # 系统内置权限配置
    #
    # 键：页面编码
    # 值：该页面下的操作权限
    PERMISSION_CONFIG = {
        "SYSTEM_USERS": [
            {
                "name": "查看用户列表",
                "code": "USER_LIST",
                "description": (
                    "允许查看系统用户列表"
                ),
                "sort_order": 10,
            },
            {
                "name": "查看用户详情",
                "code": "USER_DETAIL",
                "description": (
                    "允许查看指定用户的详细信息"
                ),
                "sort_order": 20,
            },
            {
                "name": "创建用户",
                "code": "USER_CREATE",
                "description": (
                    "允许通过用户管理接口创建用户"
                ),
                "sort_order": 30,
            },
            {
                "name": "修改用户资料",
                "code": "USER_UPDATE",
                "description": (
                    "允许修改普通用户的用户名和邮箱"
                ),
                "sort_order": 40,
            },
            {
                "name": "修改用户状态",
                "code": "USER_CHANGE_STATUS",
                "description": (
                    "允许启用或停用普通用户"
                ),
                "sort_order": 50,
            },
            {
                "name": "分配用户角色",
                "code": "USER_ASSIGN_ROLE",
                "description": (
                    "允许给普通用户分配或取消角色"
                ),
                "sort_order": 60,
            },
            {
                "name": "重置用户密码",
                "code": "USER_RESET_PASSWORD",
                "description": (
                    "允许重置普通用户密码"
                ),
                "sort_order": 70,
            },
        ],
        "SYSTEM_ROLES": [
            {
                "name": "查看角色列表",
                "code": "ROLE_LIST",
                "description": (
                    "允许查看系统角色列表"
                ),
                "sort_order": 10,
            },
            {
                "name": "查看角色详情",
                "code": "ROLE_DETAIL",
                "description": (
                    "允许查看指定角色的详细信息"
                ),
                "sort_order": 20,
            },
            {
                "name": "创建角色",
                "code": "ROLE_CREATE",
                "description": (
                    "允许创建新的系统角色"
                ),
                "sort_order": 30,
            },
            {
                "name": "修改角色资料",
                "code": "ROLE_UPDATE",
                "description": (
                    "允许修改角色名称、编码、"
                    "权重和描述"
                ),
                "sort_order": 40,
            },
            {
                "name": "修改角色状态",
                "code": "ROLE_CHANGE_STATUS",
                "description": (
                    "允许启用或停用角色"
                ),
                "sort_order": 50,
            },
        ],
        "SYSTEM_PAGES": [
            {
                "name": "查看页面列表",
                "code": "PAGE_LIST",
                "description": (
                    "允许查看系统页面列表"
                ),
                "sort_order": 10,
            },
            {
                "name": "查看页面详情",
                "code": "PAGE_DETAIL",
                "description": (
                    "允许查看指定页面的详细信息"
                ),
                "sort_order": 20,
            },
            {
                "name": "创建页面",
                "code": "PAGE_CREATE",
                "description": (
                    "允许创建新的系统页面"
                ),
                "sort_order": 30,
            },
            {
                "name": "修改页面资料",
                "code": "PAGE_UPDATE",
                "description": (
                    "允许修改页面名称、路由、"
                    "组件和父页面等资料"
                ),
                "sort_order": 40,
            },
            {
                "name": "修改页面状态",
                "code": "PAGE_CHANGE_STATUS",
                "description": (
                    "允许启用或停用页面"
                ),
                "sort_order": 50,
            },
            {
                "name": "分配页面角色",
                "code": "PAGE_ASSIGN_ROLE",
                "description": (
                    "允许配置页面对哪些角色可见"
                ),
                "sort_order": 60,
            },
        ],
    }

    @transaction.atomic
    def handle(self, *args, **options):
        """创建或更新系统操作权限"""

        required_page_codes = set(
            self.PERMISSION_CONFIG.keys()
        )

        # 一次查询获得所有需要的页面
        pages = Page.objects.filter(
            code__in=required_page_codes,
        )

        pages_by_code = {
            page.code: page
            for page in pages
        }

        # 检查系统页面是否已经创建
        missing_page_codes = (
            required_page_codes
            - set(pages_by_code.keys())
        )

        if missing_page_codes:
            missing_text = "、".join(
                sorted(missing_page_codes)
            )

            raise CommandError(
                "缺少以下系统页面："
                f"{missing_text}。"
                "请先创建页面后再初始化权限。"
            )

        created_count = 0
        updated_count = 0

        for (
            page_code,
            permission_items,
        ) in self.PERMISSION_CONFIG.items():
            page = pages_by_code[
                page_code
            ]

            for item in permission_items:
                permission, created = (
                    Permission.objects.update_or_create(
                        code=item["code"],
                        defaults={
                            "name": item["name"],
                            "page": page,
                            "description": (
                                item["description"]
                            ),
                            "sort_order": (
                                item["sort_order"]
                            ),
                            "is_active": True,
                        },
                    )
                )

                if created:
                    created_count += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            "创建权限："
                            f"{permission.code}"
                        )
                    )
                else:
                    updated_count += 1

                    self.stdout.write(
                        "更新权限："
                        f"{permission.code}"
                    )

        total_count = (
            created_count + updated_count
        )

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "RBAC 操作权限初始化完成："
                f"共处理 {total_count} 项，"
                f"新建 {created_count} 项，"
                f"更新 {updated_count} 项。"
            )
        )