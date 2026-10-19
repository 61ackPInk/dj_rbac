"""
-*- coding: utf-8 -*-
@File  : registry.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 各应用 RBAC 内置权限配置自动发现与校验
"""

from importlib import import_module

from django.apps import apps
from django.core.exceptions import (
    ImproperlyConfigured,
)


# ==================== 权限配置约定 ====================

PERMISSION_MODULE_NAME = "rbac_permissions"

REQUIRED_PERMISSION_FIELDS = {
    "name",
    "code",
    "description",
    "sort_order",
}


# ==================== 权限配置加载 ====================


def load_permission_config() -> dict:
    """发现、校验并合并各应用的权限配置。"""

    merged_config = {}
    registered_permission_codes = set()

    for app_config in apps.get_app_configs():
        module_path = (
            f"{app_config.name}."
            f"{PERMISSION_MODULE_NAME}"
        )

        try:
            permission_module = import_module(
                module_path
            )
        except ModuleNotFoundError as error:
            # 应用没有权限配置模块时正常跳过；
            # 配置模块内部导入失败时继续抛出异常。
            if error.name == module_path:
                continue

            raise

        app_permission_config = getattr(
            permission_module,
            "PERMISSION_CONFIG",
            None,
        )

        if not isinstance(
            app_permission_config,
            dict,
        ):
            raise ImproperlyConfigured(
                f"{module_path}.PERMISSION_CONFIG "
                "必须是字典"
            )

        for (
            page_code,
            permission_items,
        ) in app_permission_config.items():
            _validate_page_config(
                module_path=module_path,
                page_code=page_code,
                permission_items=(
                    permission_items
                ),
                merged_config=merged_config,
                registered_permission_codes=(
                    registered_permission_codes
                ),
            )

            merged_config[page_code] = (
                permission_items
            )

    return merged_config


# ==================== 单个页面配置校验 ====================


def _validate_page_config(
    *,
    module_path: str,
    page_code,
    permission_items,
    merged_config: dict,
    registered_permission_codes: set,
):
    """校验一个页面及其操作权限配置。"""

    if (
        not isinstance(page_code, str)
        or not page_code.strip()
    ):
        raise ImproperlyConfigured(
            f"{module_path} 包含无效页面编码"
        )

    if page_code in merged_config:
        raise ImproperlyConfigured(
            f"页面权限配置重复：{page_code}"
        )

    if not isinstance(permission_items, list):
        raise ImproperlyConfigured(
            f"{page_code} 的权限配置必须是列表"
        )

    for permission_item in permission_items:
        _validate_permission_item(
            module_path=module_path,
            page_code=page_code,
            permission_item=permission_item,
            registered_permission_codes=(
                registered_permission_codes
            ),
        )


# ==================== 单项权限配置校验 ====================


def _validate_permission_item(
    *,
    module_path: str,
    page_code: str,
    permission_item,
    registered_permission_codes: set,
):
    """校验一项操作权限配置。"""

    if not isinstance(permission_item, dict):
        raise ImproperlyConfigured(
            f"{module_path} 中 {page_code} "
            "包含非字典权限配置"
        )

    missing_fields = (
        REQUIRED_PERMISSION_FIELDS
        - set(permission_item.keys())
    )

    if missing_fields:
        missing_text = "、".join(
            sorted(missing_fields)
        )

        raise ImproperlyConfigured(
            f"{page_code} 的权限配置缺少："
            f"{missing_text}"
        )

    permission_code = permission_item[
        "code"
    ]

    if (
        not isinstance(permission_code, str)
        or not permission_code.strip()
    ):
        raise ImproperlyConfigured(
            f"{page_code} 包含无效权限编码"
        )

    if (
        permission_code
        in registered_permission_codes
    ):
        raise ImproperlyConfigured(
            "操作权限编码重复："
            f"{permission_code}"
        )

    registered_permission_codes.add(
        permission_code
    )
