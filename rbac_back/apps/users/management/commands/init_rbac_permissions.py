"""
-*- coding: utf-8 -*-
@File  : init_rbac_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 自动发现并初始化各应用的 RBAC 操作权限

python.exe manage.py init_rbac_permissions
"""

from django.core.management.base import (
    BaseCommand,
    CommandError,
)
from django.db import transaction

from apps.pages.models import Page
from apps.users.models import Permission
from common.permissions.registry import (
    load_permission_config,
)


class Command(BaseCommand):
    """初始化系统内置操作权限。"""

    help = (
        "自动发现各应用配置并创建或更新 RBAC 操作权限"
    )

    # ==================== 命令执行 ====================

    @transaction.atomic
    def handle(self, *args, **options):
        """创建或更新各应用声明的操作权限。"""

        permission_config = (
            load_permission_config()
        )

        required_page_codes = set(
            permission_config.keys()
        )

        # 一次查询获得所有需要的页面
        pages = Page.objects.filter(
            code__in=required_page_codes,
        )

        pages_by_code = {
            page.code: page
            for page in pages
        }

        # ==================== 页面完整性检查 ====================

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

        # ==================== 权限创建与更新 ====================

        for (
            page_code,
            permission_items,
        ) in permission_config.items():
            page = pages_by_code[page_code]

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
