"""
-*- coding: utf-8 -*-
@File  : __init__.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓商品库存适配器统一导出
"""

# ==================== 商品库存适配器导出 ====================

from .provider import YuanCangStockProvider

__all__ = [
    "YuanCangStockProvider",
]
