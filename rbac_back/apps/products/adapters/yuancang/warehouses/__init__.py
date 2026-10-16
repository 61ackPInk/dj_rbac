"""
-*- coding: utf-8 -*-
@File  : __init__.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓客户仓库适配器统一导出
"""

# ==================== 仓库适配器导出 ====================

from .provider import (
    YuanCangWarehouseProvider,
)

__all__ = [
    "YuanCangWarehouseProvider",
]