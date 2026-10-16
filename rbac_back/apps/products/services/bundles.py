"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品实时库存计算服务
"""

from typing import Any

from apps.products.adapters import BaseStockProvider
from apps.products.models import ProductBundle


# ==================== 组合商品服务 ====================


class BundleService:
    """根据本地组合关系和实时库存计算组合可用数量。"""

    def __init__(
        self,
        stock_provider: BaseStockProvider,
    ):
        """初始化实时库存数据提供方。"""

        self.stock_provider = stock_provider

    # ==================== 批量组合库存 ====================

    def get_available_quantity_map(
        self,
        *,
        provider_code: str,
        warehouse_code: str,
    ) -> dict[int, int]:
        """
        计算指定来源、指定仓库下的有效组合库存。

        返回值以本地组合商品主键作为键，方便后续
        列表和详情接口把实时库存合并到组合资料。
        """

        normalized_provider_code = (
            provider_code.strip()
        )
        normalized_warehouse_code = (
            warehouse_code.strip()
        )

        if not normalized_provider_code:
            raise ValueError(
                "数据来源编码不能为空"
            )

        if not normalized_warehouse_code:
            raise ValueError(
                "仓库编码不能为空"
            )

        bundles = list(
            ProductBundle.objects.filter(
                provider_code=(
                    normalized_provider_code
                ),
                is_active=True,
            ).prefetch_related("items")
        )

        if not bundles:
            return {}

        customer_skus = sorted({
            item.customer_sku
            for bundle in bundles
            for item in bundle.items.all()
            if item.customer_sku
        })

        stock_map = {}

        if customer_skus:
            stock_map = (
                self.stock_provider
                .get_stock_list(
                    normalized_warehouse_code,
                    customer_skus,
                )
            )

        return {
            bundle.id: (
                self._calculate_available_quantity(
                    bundle=bundle,
                    stock_map=stock_map,
                )
            )
            for bundle in bundles
        }

    # ==================== 单个组合库存计算 ====================

    @classmethod
    def _calculate_available_quantity(
        cls,
        *,
        bundle: ProductBundle,
        stock_map: dict[str, dict[str, Any]],
    ) -> int:
        """计算一个组合商品的实时可用数量。"""

        item_quantities = []

        for item in bundle.items.all():
            stock = stock_map.get(
                item.customer_sku
            )

            available = cls._read_available(
                stock
            )

            item_quantities.append(
                available
                // item.required_quantity
            )

        # 没有组成明细的组合无法组成，按0处理。
        if not item_quantities:
            return 0

        return min(item_quantities)

    # ==================== 库存数值读取 ====================

    @staticmethod
    def _read_available(
        stock: dict[str, Any] | None,
    ) -> int:
        """读取实时可用库存，缺失或无效数值按0处理。"""

        if not isinstance(stock, dict):
            return 0

        raw_available = stock.get(
            "available"
        )

        try:
            available = int(raw_available)
        except (TypeError, ValueError):
            return 0

        return max(available, 0)
