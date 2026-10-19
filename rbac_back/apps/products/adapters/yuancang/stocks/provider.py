"""
-*- coding: utf-8 -*-
@File  : provider.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓商品库存数据适配器
"""

from typing import Any

from apps.products.adapters.base import (
    BaseStockProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)

from ..common.client import YuanCangClient
from .endpoints import (
    YUANCANG_STOCK_LIST_PATH,
)
from .mappers import map_stock_item


# ==================== 元仓库存适配器 ====================


class YuanCangStockProvider(
    BaseStockProvider
):
    """批量读取并转换元仓商品库存。"""

    def __init__(
        self,
        client: YuanCangClient | None = None,
    ):
        self.client = (
            client or YuanCangClient()
        )

    # ==================== 批量库存查询 ====================

    def get_stock_list(
        self,
        warehouse_code: str,
        customer_skus: list[str],
    ) -> dict[str, dict[str, Any]]:
        """
        查询指定仓库中的多个商品库存。

        商品列表每页最多100条，
        因此一次库存请求不会超过100个SKU。
        """

        if not customer_skus:
            return {}

        source_data = self.client.post(
            YUANCANG_STOCK_LIST_PATH,
            {
                "warehouseCode": (
                    warehouse_code
                ),
                "page": 1,
                "prePage": len(
                    customer_skus
                ),
                "customerSku": (
                    customer_skus
                ),
            },
        )

        if not isinstance(source_data, dict):
            raise ProductProviderResponseError(
                "元仓库存列表响应缺少 data"
            )

        source_items = source_data.get(
            "list"
        )

        if not isinstance(source_items, list):
            raise ProductProviderResponseError(
                "元仓库存列表响应缺少 list"
            )

        stock_map = {}

        for source_item in source_items:
            if not isinstance(
                source_item,
                dict,
            ):
                continue

            stock = map_stock_item(
                source_item
            )
            customer_sku = stock.get(
                "customer_sku"
            )

            if customer_sku:
                stock_map[customer_sku] = (
                    stock
                )

        return stock_map
