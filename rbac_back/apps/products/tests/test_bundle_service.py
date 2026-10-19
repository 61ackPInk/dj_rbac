"""
-*- coding: utf-8 -*-
@File  : test_bundle_service.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品实时库存计算服务测试
"""

from unittest.mock import Mock

from django.test import TestCase
from django.utils import timezone

from apps.products.adapters import BaseStockProvider
from apps.products.models import (
    ProductBundle,
    ProductBundleItem,
)
from apps.products.services import BundleService


class BundleServiceTests(TestCase):
    """组合商品实时库存计算服务测试。"""

    def setUp(self):
        """初始化库存 Provider 和组合服务。"""

        self.stock_provider = Mock(
            spec=BaseStockProvider
        )
        self.service = BundleService(
            stock_provider=self.stock_provider
        )

    # ==================== 测试数据构造 ====================

    def create_bundle(
        self,
        *,
        external_id: str,
        bundle_sku: str,
        name: str | None = None,
        is_active: bool = True,
    ) -> ProductBundle:
        """创建组合商品测试数据。"""

        return ProductBundle.objects.create(
            provider_code="yuancang",
            external_id=external_id,
            bundle_sku=bundle_sku,
            name=(name or f"测试组合-{bundle_sku}"),
            collected_at=timezone.now(),
            is_active=is_active,
        )

    @staticmethod
    def create_item(
            *,
            bundle: ProductBundle,
            customer_sku: str,
            required_quantity: int,
            provider_sku: str = "",
            name: str = "",
    ) -> ProductBundleItem:
        """创建组合子商品测试数据。"""

        return ProductBundleItem.objects.create(
            bundle=bundle,
            provider_sku=provider_sku,
            customer_sku=customer_sku,
            name=name,
            required_quantity=required_quantity,
        )

    # ==================== 组合库存计算 ====================

    def test_calculates_inventory_from_child_skus(
        self,
    ):
        """组合库存应取各子SKU可组成数量的最小值。"""

        bundle = self.create_bundle(
            external_id="1",
            bundle_sku="BUNDLE-001",
        )
        self.create_item(
            bundle=bundle,
            customer_sku="SKU-A",
            required_quantity=1,
        )
        self.create_item(
            bundle=bundle,
            customer_sku="SKU-B",
            required_quantity=2,
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-A": {
                "available": 7,
            },
            "SKU-B": {
                "available": 5,
            },
        }

        result = self.service.get_available_quantity_map(
            provider_code="yuancang",
            warehouse_code="HK01",
        )

        self.assertEqual(
            result,
            {
                bundle.id: 2,
            },
        )
        self.stock_provider.get_stock_list.assert_called_once_with(
            "HK01",
            [
                "SKU-A",
                "SKU-B",
            ],
        )

    def test_missing_child_stock_returns_zero(
        self,
    ):
        """任一子SKU库存缺失时组合库存应为0。"""

        bundle = self.create_bundle(
            external_id="2",
            bundle_sku="BUNDLE-002",
        )
        self.create_item(
            bundle=bundle,
            customer_sku="SKU-A",
            required_quantity=1,
        )
        self.create_item(
            bundle=bundle,
            customer_sku="SKU-MISSING",
            required_quantity=1,
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-A": {
                "available": 10,
            },
        }

        result = self.service.get_available_quantity_map(
            provider_code="yuancang",
            warehouse_code="HK01",
        )

        self.assertEqual(result[bundle.id], 0)

    def test_ignores_inactive_bundles(self):
        """库存计算不应包含已经失效的组合。"""

        active_bundle = self.create_bundle(
            external_id="3",
            bundle_sku="BUNDLE-003",
        )
        inactive_bundle = self.create_bundle(
            external_id="4",
            bundle_sku="BUNDLE-004",
            is_active=False,
        )
        self.create_item(
            bundle=active_bundle,
            customer_sku="SKU-A",
            required_quantity=1,
        )
        self.create_item(
            bundle=inactive_bundle,
            customer_sku="SKU-B",
            required_quantity=1,
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-A": {
                "available": 6,
            },
            "SKU-B": {
                "available": 9,
            },
        }

        result = self.service.get_available_quantity_map(
            provider_code="yuancang",
            warehouse_code="HK01",
        )

        self.assertEqual(
            result,
            {
                active_bundle.id: 6,
            },
        )
        self.stock_provider.get_stock_list.assert_called_once_with(
            "HK01",
            ["SKU-A"],
        )

    def test_empty_active_bundle_list_skips_stock_request(
        self,
    ):
        """没有有效组合时不应请求第三方库存。"""

        result = self.service.get_available_quantity_map(
            provider_code="yuancang",
            warehouse_code="HK01",
        )

        self.assertEqual(result, {})
        self.stock_provider.get_stock_list.assert_not_called()

    def test_requires_warehouse_code(self):
        """计算组合库存必须提供仓库编码。"""

        with self.assertRaisesMessage(
            ValueError,
            "仓库编码不能为空",
        ):
            self.service.get_available_quantity_map(
                provider_code="yuancang",
                warehouse_code=" ",
            )

    # ==================== 组合列表测试 ====================

    def test_bundle_list_paginates_before_stock_request(
        self,
    ):
        """组合列表只查询当前页涉及的子SKU库存。"""

        first_bundle = self.create_bundle(
            external_id="10",
            bundle_sku="BUNDLE-001",
        )
        second_bundle = self.create_bundle(
            external_id="11",
            bundle_sku="BUNDLE-002",
        )

        self.create_item(
            bundle=first_bundle,
            customer_sku="SKU-A",
            required_quantity=1,
        )
        self.create_item(
            bundle=second_bundle,
            provider_sku="ERP-SKU-B",
            customer_sku="SKU-B",
            name="测试子商品B",
            required_quantity=2,
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-B": {
                "available": 9,
            },
        }

        result = self.service.get_bundle_list(
            provider_code="yuancang",
            query={
                "warehouse_code": "HK01",
                "page": 2,
                "page_size": 1,
            },
        )

        self.assertEqual(
            result["pagination"],
            {
                "page": 2,
                "page_size": 1,
                "total": 2,
            },
        )
        self.assertEqual(
            len(result["items"]),
            1,
        )
        self.assertEqual(
            result["items"][0][
                "bundle_sku"
            ],
            "BUNDLE-002",
        )
        self.assertEqual(
            result["items"][0][
                "available_quantity"
            ],
            4,
        )
        self.assertEqual(
            result["items"][0][
                "item_count"
            ],
            1,
        )

        components = result["items"][0][
            "components"
        ]

        self.assertEqual(
            len(components),
            1,
        )

        self.assertEqual(
            components[0]["provider_sku"],
            "ERP-SKU-B",
        )

        self.assertEqual(
            components[0]["customer_sku"],
            "SKU-B",
        )

        self.assertEqual(
            components[0]["name"],
            "测试子商品B",
        )

        self.assertEqual(
            components[0][
                "required_quantity"
            ],
            2,
        )

        self.stock_provider.get_stock_list.assert_called_once_with(
            "HK01",
            ["SKU-B"],
        )

    def test_bundle_list_filters_by_sku_and_name(
        self,
    ):
        """组合列表支持按组合SKU和名称筛选。"""

        matched_bundle = self.create_bundle(
            external_id="20",
            bundle_sku="SET-001-A",
            name="咖啡杯组合",
        )
        self.create_bundle(
            external_id="21",
            bundle_sku="SET-002-A",
            name="铃兰杯组合",
        )

        self.create_item(
            bundle=matched_bundle,
            customer_sku="SKU-A",
            required_quantity=1,
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-A": {
                "available": 12,
            },
        }

        result = self.service.get_bundle_list(
            provider_code="yuancang",
            query={
                "warehouse_code": "HK01",
                "page": 1,
                "page_size": 20,
                "bundle_sku": "SET-001",
                "name": "咖啡",
            },
        )

        self.assertEqual(
            result["pagination"]["total"],
            1,
        )
        self.assertEqual(
            result["items"][0][
                "bundle_sku"
            ],
            "SET-001-A",
        )
        self.assertEqual(
            result["items"][0][
                "warehouse_code"
            ],
            "HK01",
        )
        self.assertEqual(
            result["items"][0][
                "available_quantity"
            ],
            12,
        )

    # ==================== 组合详情测试 ====================

    def test_bundle_detail_returns_component_stock(
        self,
    ):
        """组合详情应返回组成商品及实时库存。"""

        bundle = self.create_bundle(
            external_id="30",
            bundle_sku="SET-003-A",
            name="测试组合详情",
        )

        first_item = self.create_item(
            bundle=bundle,
            provider_sku="ERP-SKU-A",
            customer_sku="SKU-A",
            name="测试子商品A",
            required_quantity=1,
        )
        first_item.image_url = (
            "https://example.com/a.png"
        )
        first_item.save(
            update_fields=["image_url"]
        )

        second_item = self.create_item(
            bundle=bundle,
            provider_sku="ERP-SKU-B",
            customer_sku="SKU-B",
            name="测试子商品B",
            required_quantity=2,
        )
        second_item.image_url = (
            "https://example.com/b.png"
        )
        second_item.save(
            update_fields=["image_url"]
        )

        self.stock_provider.get_stock_list.return_value = {
            "SKU-A": {
                "available": 20,
            },
            "SKU-B": {
                "available": 25,
            },
        }

        result = self.service.get_bundle_detail(
            provider_code="yuancang",
            bundle_id=bundle.id,
            query={
                "warehouse_code": "055",
            },
        )

        self.assertEqual(
            result["bundle_sku"],
            "SET-003-A",
        )
        self.assertEqual(
            result["warehouse_code"],
            "055",
        )
        self.assertEqual(
            result["available_quantity"],
            12,
        )
        self.assertEqual(
            result["item_count"],
            2,
        )

        components = result["components"]

        self.assertEqual(
            components[0]["customer_sku"],
            "SKU-A",
        )
        self.assertEqual(
            components[0][
                "available_quantity"
            ],
            20,
        )
        self.assertEqual(
            components[0][
                "producible_quantity"
            ],
            20,
        )
        self.assertEqual(
            components[0]["image_url"],
            "https://example.com/a.png",
        )

        self.assertEqual(
            components[1][
                "available_quantity"
            ],
            25,
        )
        self.assertEqual(
            components[1][
                "producible_quantity"
            ],
            12,
        )

        self.stock_provider.get_stock_list.assert_called_once_with(
            "055",
            [
                "SKU-A",
                "SKU-B",
            ],
        )

    def test_bundle_detail_missing_stock_uses_zero(
        self,
    ):
        """子SKU库存缺失时详情和组合库存均按0处理。"""

        bundle = self.create_bundle(
            external_id="31",
            bundle_sku="SET-004-A",
        )
        self.create_item(
            bundle=bundle,
            customer_sku="SKU-MISSING",
            required_quantity=2,
        )

        self.stock_provider.get_stock_list.return_value = {}

        result = self.service.get_bundle_detail(
            provider_code="yuancang",
            bundle_id=bundle.id,
            query={
                "warehouse_code": "055",
            },
        )

        self.assertEqual(
            result["available_quantity"],
            0,
        )
        self.assertEqual(
            result["components"][0][
                "available_quantity"
            ],
            0,
        )
        self.assertEqual(
            result["components"][0][
                "producible_quantity"
            ],
            0,
        )

    def test_bundle_detail_rejects_blank_warehouse(
        self,
    ):
        """组合详情必须提供仓库编码。"""

        bundle = self.create_bundle(
            external_id="32",
            bundle_sku="SET-005-A",
        )

        with self.assertRaisesMessage(
            ValueError,
            "仓库编码不能为空",
        ):
            self.service.get_bundle_detail(
                provider_code="yuancang",
                bundle_id=bundle.id,
                query={
                    "warehouse_code": " ",
                },
            )

        self.stock_provider.get_stock_list.assert_not_called()

    def test_bundle_detail_excludes_inactive_bundle(
        self,
    ):
        """已经失效的组合不能通过详情服务查询。"""

        bundle = self.create_bundle(
            external_id="33",
            bundle_sku="SET-006-A",
            is_active=False,
        )

        with self.assertRaises(
            ProductBundle.DoesNotExist,
        ):
            self.service.get_bundle_detail(
                provider_code="yuancang",
                bundle_id=bundle.id,
                query={
                    "warehouse_code": "055",
                },
            )

        self.stock_provider.get_stock_list.assert_not_called()
