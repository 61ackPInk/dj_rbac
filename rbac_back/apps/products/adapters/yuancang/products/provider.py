"""
-*- coding: utf-8 -*-
@File  : provider.py
@Author: 61ackPink
@Time : 2026/10/10 17:06
@Desc : 元仓普通商品数据适配器
"""
from typing import Any

from apps.products.adapters import (
    BaseProductProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)

from ..common.client import YuanCangClient
from .endpoints import (
    YUANCANG_PRODUCT_DETAIL_PATH,
    YUANCANG_PRODUCT_LIST_PATH,
)
from .mappers import (
    map_product_detail,
    map_product_list_item,
    map_product_list_query,
)


# ==================== 元仓普通商品适配器 ====================


class YuanCangProductProvider(
    BaseProductProvider
):
    """将元仓商品数据转换为本系统统一结构。"""

    def __init__(
        self,
        client: YuanCangClient | None = None,
    ):
        self.client = (
            client or YuanCangClient()
        )

    # ==================== 商品列表 ====================

    def get_product_list(
        self,
        query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取并转换元仓商品列表。"""

        source_data = self.client.post(
            YUANCANG_PRODUCT_LIST_PATH,
            map_product_list_query(query),
        )

        if not isinstance(source_data, dict):
            raise ProductProviderResponseError(
                "元仓商品列表响应缺少 data"
            )

        source_items = source_data.get(
            "list"
        )

        if not isinstance(source_items, list):
            raise ProductProviderResponseError(
                "元仓商品列表响应缺少 list"
            )

        items = [
            map_product_list_item(item)
            for item in source_items
            if isinstance(item, dict)
        ]

        return {
            "items": items,
            "pagination": {
                "page": source_data.get(
                    "page"
                ),
                "page_size": source_data.get(
                    "prePage"
                ),
                "total": source_data.get(
                    "total"
                ),
            },
        }

    # ==================== 商品详情 ====================

    def get_product_detail(
        self,
        customer_sku: str,
    ) -> dict[str, Any]:
        """根据客户 SKU 获取并转换商品详情。"""

        source_data = self.client.post(
            YUANCANG_PRODUCT_DETAIL_PATH,
            {
                "customerSku": customer_sku,
            },
        )

        if not isinstance(source_data, dict):
            raise ProductProviderResponseError(
                "元仓商品详情响应缺少 data"
            )

        return map_product_detail(
            source_data
        )
