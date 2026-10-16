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

    # ==================== 组合商品列表 ====================

    def get_bundle_list(
        self,
        *,
        provider_code: str,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取包含指定仓库实时库存的组合列表。"""

        # ==================== 参数标准化 ====================

        normalized_provider_code = (
            provider_code.strip()
        )
        warehouse_code = str(
            query.get(
                "warehouse_code",
                "",
            )
        ).strip()

        if not normalized_provider_code:
            raise ValueError(
                "数据来源编码不能为空"
            )

        if not warehouse_code:
            raise ValueError(
                "仓库编码不能为空"
            )

        page = query.get("page", 1)
        page_size = query.get(
            "page_size",
            20,
        )

        # ==================== 本地组合查询 ====================

        queryset = ProductBundle.objects.filter(
            provider_code=normalized_provider_code,
            is_active=True,
        )

        bundle_sku = query.get("bundle_sku")

        if bundle_sku:
            queryset = queryset.filter(
                bundle_sku__icontains=(
                    bundle_sku
                )
            )

        name = query.get("name")

        if name:
            queryset = queryset.filter(
                name__icontains=name
            )

        total = queryset.count()

        # ==================== 当前页数据 ====================

        start_index = (
            page - 1
        ) * page_size
        end_index = (
            start_index + page_size
        )

        bundles = list(
            queryset.prefetch_related(
                "items"
            )[
                start_index:end_index
            ]
        )

        # 只查询当前页组合涉及的子SKU库存
        stock_map = self._load_stock_map(
            bundles=bundles,
            warehouse_code=warehouse_code,
        )

        # ==================== 统一列表结构 ====================

        items = []

        for bundle in bundles:
            bundle_items = list(
                bundle.items.all()
            )

            items.append({
                "id": bundle.id,
                "bundle_sku": (
                    bundle.bundle_sku
                ),
                "name": bundle.name,
                "image_url": (
                    bundle.image_url
                ),
                "source_status": (
                    bundle.source_status
                ),
                "source_status_name": (
                    bundle.source_status_name
                ),
                "warehouse_code": (
                    warehouse_code
                ),
                "available_quantity": (
                    self
                    ._calculate_available_quantity(
                        bundle=bundle,
                        stock_map=stock_map,
                    )
                ),
                "item_count": len(
                    bundle_items
                ),
                "collected_at": (
                    bundle.collected_at
                ),
            })

        return {
            "items": items,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
            },
        }

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

        stock_map = self._load_stock_map(
            bundles=bundles,
            warehouse_code=(
                normalized_warehouse_code
            ),
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

    # ==================== 批量库存加载 ====================

    def _load_stock_map(
        self,
        *,
        bundles: list[ProductBundle],
        warehouse_code: str,
    ) -> dict[str, dict[str, Any]]:
        """查询指定仓库中当前组合需要的全部子SKU库存。"""

        customer_skus = sorted({
            item.customer_sku
            for bundle in bundles
            for item in bundle.items.all()
            if item.customer_sku
        })

        if not customer_skus:
            return {}

        return self.stock_provider.get_stock_list(
            warehouse_code,
            customer_skus,
        )

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
