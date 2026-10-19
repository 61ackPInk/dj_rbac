"""
-*- coding: utf-8 -*-
@File  : mappers.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓仓库字段与统一结构转换
"""

from typing import Any


# ==================== 基础字段转换 ====================


def _string_id(value: Any) -> str | None:
    """将不同 ERP 的仓库标识统一转换为字符串。"""

    if value is None:
        return None

    return str(value)


# ==================== 仓库字段转换 ====================


def map_warehouse_item(
    source: dict[str, Any],
) -> dict[str, Any]:
    """将元仓仓库记录转换为统一结构。"""

    return {
        "id": _string_id(
            source.get("id")
        ),
        "code": source.get("code"),
        "name": source.get("name"),
        "site_code": source.get(
            "siteCode"
        ),
        "address": source.get(
            "address"
        ),
        "contact_name": source.get(
            "contacts"
        ),
        "contact_phone": source.get(
            "phone"
        ),
    }