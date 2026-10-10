"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/10 16:28
@Desc : 
"""
from typing import Any

from apps.products.adapters import BaseProductProvider


# ==================== 组合商品服务 ====================


class BundleService:
    """
    组合商品业务服务。

    View 通过当前服务获取组合商品数据，
    不直接调用元仓或其他 ERP 适配器。
    """

    def __init__(
        self,
        provider: BaseProductProvider,
    ):
        self.provider = provider

    # ==================== 组合商品列表 ====================

    def get_bundle_list(
        self,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取统一结构的组合商品列表。"""

        return self.provider.get_bundle_list(
            query,
        )

    # ==================== 组合商品详情 ====================

    def get_bundle_detail(
        self,
        bundle_id: str,
    ) -> dict[str, Any]:
        """获取统一结构的组合商品详情。"""

        return self.provider.get_bundle_detail(
            bundle_id,
        )