"""
-*- coding: utf-8 -*-
@File  : test_product_service.py
@Author: 61ackPink
@Time : 2026/10/12 11:41
@Desc : 商品资料与实时库存业务编排测试
"""

from unittest.mock import (
    Mock,
    call,
)

from django.test import SimpleTestCase

from apps.products.adapters import (
    BaseProductProvider,
    BaseStockProvider,
)
from apps.products.services import ProductService


class ProductServiceTests(SimpleTestCase):
    """商品服务层测试。"""

    def setUp(self):
        """创建测试使用的假 Provider。"""

        self.product_provider = Mock(
            spec=BaseProductProvider,
        )
        self.stock_provider = Mock(
            spec=BaseStockProvider,
        )

        self.service = ProductService(
            product_provider=(
                self.product_provider
            ),
            stock_provider=(
                self.stock_provider
            ),
        )

    # ====================
    # 按仓库批量查询库存
    # ====================

    def test_product_list_groups_stock_by_warehouse(
        self,
    ):
        """同仓库SKU应合并为一次库存请求。"""

        self.product_provider.get_product_list.return_value = {
            "items": [
                {
                    "customer_sku": "SKU-A",
                    "main_warehouse": {
                        "code": "WAREHOUSE-A",
                    },
                },
                {
                    "customer_sku": "SKU-B",
                    "main_warehouse": {
                        "code": "WAREHOUSE-A",
                    },
                },
                {
                    "customer_sku": "SKU-C",
                    "main_warehouse": {
                        "code": "WAREHOUSE-B",
                    },
                },
            ],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total": 3,
            },
        }

        def stock_side_effect(
            warehouse_code,
            customer_skus,
        ):
            if warehouse_code == "WAREHOUSE-A":
                return {
                    "SKU-A": {
                        "found": True,
                        "warehouse_code": (
                            "WAREHOUSE-A"
                        ),
                        "available": 100,
                    },
                    "SKU-B": {
                        "found": True,
                        "warehouse_code": (
                            "WAREHOUSE-A"
                        ),
                        "available": 80,
                    },
                }

            return {
                "SKU-C": {
                    "found": True,
                    "warehouse_code": (
                        "WAREHOUSE-B"
                    ),
                    "available": 75,
                },
            }

        self.stock_provider.get_stock_list.side_effect = (
            stock_side_effect
        )

        result = self.service.get_product_list({
            "page": 1,
            "page_size": 20,
        })

        # 同一仓库的SKU必须通过一次请求查询
        self.assertEqual(
            self.stock_provider
            .get_stock_list.call_args_list,
            [
                call(
                    "WAREHOUSE-A",
                    [
                        "SKU-A",
                        "SKU-B",
                    ],
                ),
                call(
                    "WAREHOUSE-B",
                    [
                        "SKU-C",
                    ],
                ),
            ],
        )

        # 库存必须合并回对应商品
        self.assertEqual(
            result["items"][0]["inventory"][
                "available"
            ],
            100,
        )
        self.assertEqual(
            result["items"][1]["inventory"][
                "available"
            ],
            80,
        )
        self.assertEqual(
            result["items"][2]["inventory"][
                "available"
            ],
            75,
        )

    # ====================
    # 未匹配库存处理
    # ====================

    def test_missing_stock_returns_null_quantities(
        self,
    ):
        """未找到库存时不能错误地返回零库存。"""

        self.product_provider.get_product_list.return_value = {
            "items": [
                {
                    "customer_sku": "SKU-NOT-FOUND",
                    "main_warehouse": {
                        "code": "WAREHOUSE-A",
                    },
                },
            ],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total": 1,
            },
        }

        self.stock_provider.get_stock_list.return_value = {}

        result = self.service.get_product_list({
            "page": 1,
            "page_size": 20,
        })

        inventory = result["items"][0][
            "inventory"
        ]

        self.assertFalse(
            inventory["found"]
        )
        self.assertEqual(
            inventory["warehouse_code"],
            "WAREHOUSE-A",
        )

        quantity_fields = [
            "preparing",
            "transferring",
            "waiting_for_shelf",
            "total",
            "occupied",
            "unshipped",
            "available",
        ]

        for field_name in quantity_fields:
            with self.subTest(
                field_name=field_name,
            ):
                self.assertIsNone(
                    inventory[field_name]
                )