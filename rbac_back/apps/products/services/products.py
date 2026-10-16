"""
-*- coding: utf-8 -*-
@File  : provider.py
@Author: 61ackPink
@Time : 2026/10/10 17:53
@Desc : 普通商品资料与实时库存业务编排
"""

from typing import Any

from apps.products.adapters import (
    BaseProductProvider,
    BaseStockProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)


# ==================== 普通商品服务 ====================


class ProductService:
    """
    普通商品业务服务。

    负责获取商品资料、按主仓库批量查询库存，
    并通过 customer_sku 合并统一结果。
    """

    def __init__(
            self,
            product_provider: BaseProductProvider,
            stock_provider: BaseStockProvider,
    ):
        self.product_provider = (
            product_provider
        )
        self.stock_provider = (
            stock_provider
        )

    # ==================== 商品列表 ====================

    def get_product_list(
            self,
            query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取包含实时库存的商品列表。"""

        result = (
            self.product_provider
            .get_product_list(query)
        )

        if not isinstance(result, dict):
            raise ProductProviderResponseError(
                "商品Provider返回格式错误"
            )

        items = result.get("items")

        if not isinstance(items, list):
            raise ProductProviderResponseError(
                "商品Provider返回结果缺少items"
            )

        warehouse_groups = (
            self._group_products_by_warehouse(
                items
            )
        )

        stock_map = (
            self._load_stock_map(
                warehouse_groups
            )
        )

        self._merge_product_stock(
            items,
            stock_map,
        )

        return result

    # ==================== 商品详情 ====================

    def get_product_detail(
            self,
            customer_sku: str,
    ) -> dict[str, Any]:
        """获取包含实时库存的商品详情。"""

        product = (
            self.product_provider
            .get_product_detail(
                customer_sku
            )
        )

        if not isinstance(product, dict):
            raise ProductProviderResponseError(
                "商品详情Provider返回格式错误"
            )

        product_customer_sku = (
                product.get("customer_sku")
                or customer_sku
        )

        main_warehouse = product.get(
            "main_warehouse"
        )
        warehouse_code = None

        if isinstance(main_warehouse, dict):
            warehouse_code = (
                main_warehouse.get("code")
            )

        stock = None

        if (
                warehouse_code
                and product_customer_sku
        ):
            stock_map = (
                self.stock_provider
                .get_stock_list(
                    warehouse_code,
                    [
                        product_customer_sku,
                    ],
                )
            )

            stock = stock_map.get(
                product_customer_sku
            )

        if stock is None:
            stock = self._create_missing_stock(
                warehouse_code
            )

        product["inventory"] = stock

        return product

    # ==================== 按主仓库分组 ====================

    @staticmethod
    def _group_products_by_warehouse(
            items: list[dict[str, Any]],
    ) -> dict[str, list[str]]:
        """
        将当前页商品按照主仓库分组。

        同一个仓库中的多个SKU可以通过一次
        元仓库存列表请求批量查询。
        """

        groups = {}

        for item in items:
            if not isinstance(item, dict):
                continue

            customer_sku = item.get(
                "customer_sku"
            )
            main_warehouse = item.get(
                "main_warehouse"
            )

            if not isinstance(
                    main_warehouse,
                    dict,
            ):
                continue

            warehouse_code = (
                main_warehouse.get("code")
            )

            if (
                    not customer_sku
                    or not warehouse_code
            ):
                continue

            warehouse_skus = (
                groups.setdefault(
                    warehouse_code,
                    [],
                )
            )

            # 防止同一页重复SKU造成重复查询
            if customer_sku not in warehouse_skus:
                warehouse_skus.append(
                    customer_sku
                )

        return groups

    # ==================== 批量加载库存 ====================

    def _load_stock_map(
            self,
            warehouse_groups: dict[
                str,
                list[str],
            ],
    ) -> dict[
        tuple[str, str],
        dict[str, Any],
    ]:
        """
        按仓库批量读取库存。

        使用“仓库编码 + 客户SKU”作为键，
        避免未来不同仓库出现相同SKU时相互覆盖。
        """

        stock_map = {}

        for (
                warehouse_code,
                customer_skus,
        ) in warehouse_groups.items():
            warehouse_stock = (
                self.stock_provider
                .get_stock_list(
                    warehouse_code,
                    customer_skus,
                )
            )

            for (
                    customer_sku,
                    stock,
            ) in warehouse_stock.items():
                stock_map[
                    (
                        warehouse_code,
                        customer_sku,
                    )
                ] = stock

        return stock_map

    # ==================== 合并商品和库存 ====================

    def _merge_product_stock(
            self,
            items: list[dict[str, Any]],
            stock_map: dict[
                tuple[str, str],
                dict[str, Any],
            ],
    ):
        """把实时库存写入对应商品。"""

        for item in items:
            customer_sku = item.get(
                "customer_sku"
            )
            main_warehouse = item.get(
                "main_warehouse"
            )

            warehouse_code = None

            if isinstance(
                    main_warehouse,
                    dict,
            ):
                warehouse_code = (
                    main_warehouse.get("code")
                )

            stock = stock_map.get(
                (
                    warehouse_code,
                    customer_sku,
                )
            )

            if stock is None:
                stock = (
                    self._create_missing_stock(
                        warehouse_code
                    )
                )

            item["inventory"] = stock

    # ==================== 未匹配库存结构 ====================

    @staticmethod
    def _create_missing_stock(
            warehouse_code: str | None,
    ) -> dict[str, Any]:
        """
        创建未匹配库存结构。

        未查到库存不等于库存为0，
        因此所有数量字段返回null。
        """

        return {
            "found": False,
            "warehouse_code": (
                warehouse_code
            ),
            "site_code": None,
            "preparing": None,
            "transferring": None,
            "waiting_for_shelf": None,
            "total": None,
            "occupied": None,
            "unshipped": None,
            "available": None,
            "status_name": None,
            "lock_status_name": None,
        }
