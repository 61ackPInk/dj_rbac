"""
-*- coding: utf-8 -*-
@File  : mappers.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓商品库存字段与统一结构转换
"""

from typing import Any


# ==================== 商品库存字段 ====================


def map_stock_item(
        source: dict[str, Any],
) -> dict[str, Any]:
    """将元仓库存记录转换为统一结构。"""

    return {
        "found": True,
        "warehouse_code": source.get(
            "warehouseCode"
        ),
        "site_code": source.get(
            "siteCode"
        ),
        "customer_sku": source.get(
            "customerSku"
        ),
        "preparing": source.get(
            "prepare"
        ),
        "transferring": source.get(
            "transfer"
        ),
        "waiting_for_shelf": source.get(
            "waitShelf"
        ),
        "total": source.get(
            "inventory"
        ),
        "occupied": source.get(
            "occupy"
        ),
        "unshipped": source.get(
            "unshipped"
        ),
        "available": source.get(
            "available"
        ),
        "status_name": source.get(
            "statusDes"
        ),
        "lock_status_name": source.get(
            "isLockDes"
        ),
    }
