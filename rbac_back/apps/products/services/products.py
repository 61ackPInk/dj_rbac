"""
-*- coding: utf-8 -*-
@File  : products.py
@Author: 61ackPink
@Time : 2026/10/10 16:28
@Desc : 
"""
from typing import Any

from apps.products.adapters import BaseProductProvider


# ==================== 普通商品服务 ====================


class ProductService:
    """
    普通商品业务服务。

    View 只调用当前服务，不直接访问元仓适配器。
    更换 ERP 时，只需要替换传入的适配器实现。
    """

    def __init__(
        self,
        provider: BaseProductProvider,
    ):
        self.provider = provider

    # ==================== 商品列表 ====================

    def get_product_list(
        self,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取统一结构的普通商品列表。"""

        return self.provider.get_product_list(
            query,
        )

    # ==================== 商品详情 ====================
    
    def get_product_detail(
            self,
            customer_sku: str,
    ) -> dict[str, Any]:
        """根据客户 SKU 获取统一商品详情。"""

        return self.provider.get_product_detail(
            customer_sku,
        )