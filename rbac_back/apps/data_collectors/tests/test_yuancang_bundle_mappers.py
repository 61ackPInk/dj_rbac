"""
-*- coding: utf-8 -*-
@File  : test_yuancang_bundle_mappers.py
@Author: 61ackPink
@Time : 2026/10/15 14:39
@Desc : 元仓组合商品采集转换测试
"""

from django.test import SimpleTestCase
from django.utils import timezone

from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.data_collectors.collectors.yuancang.mappers.bundle_mappings import (
    map_bundle_list_response,
    map_bundle_record,
)


class YuancangBundleMapperTests(SimpleTestCase):
    """元仓组合商品 Mapper 测试。"""

    def create_source_record(self):
        """创建元仓组合商品测试数据。"""

        return {
            "id": 496030,
            "originSku": "SET-002-SUPER-1",
            "originSkuName": "铃兰杯礼盒",
            "imageUrls": "https://example.com/bundle.png",
            "createdAt": "2026-10-13 20:13:25",
            "updatedAt": "2026-10-13 20:13:25",
            "statusDescription": "启用",
            "status": 1,
            "mapItemList": [
                {
                    "productSku": (
                        "YC7832-SET-002-SUPER"
                    ),
                    "customerSku": "SET-002-SUPER",
                    "productName": "铃兰杯礼盒",
                    "productStatus": 1,
                    "productStatusDescription": "正常",
                    "quantity": 1,
                    "imageUrl": (
                        "https://example.com/item.png"
                    ),
                },
                {
                    "productSku": (
                        "YC7832-white-bag-s"
                    ),
                    "customerSku": "white-bag-s",
                    "productName": "白色礼品袋",
                    "productStatus": 1,
                    "productStatusDescription": "正常",
                    "quantity": 1,
                    "imageUrl": (
                        "https://example.com/bag.png"
                    ),
                },
            ],
        }

    def test_map_bundle_record(self):
        """可以转换单个元仓组合商品。"""

        result = map_bundle_record(
            self.create_source_record()
        )

        self.assertEqual(
            result.provider_code,
            "yuancang",
        )
        self.assertEqual(
            result.external_id,
            "496030",
        )
        self.assertEqual(
            result.bundle_sku,
            "SET-002-SUPER-1",
        )
        self.assertEqual(
            result.source_status,
            "1",
        )
        self.assertEqual(
            len(result.items),
            2,
        )
        self.assertEqual(
            result.items[1].customer_sku,
            "white-bag-s",
        )
        self.assertEqual(
            result.items[1].required_quantity,
            1,
        )
        self.assertTrue(
            timezone.is_aware(
                result.source_created_at
            )
        )

    def test_duplicate_customer_sku_is_merged(self):
        """相同子SKU会合并并累加数量。"""

        source = self.create_source_record()

        source["mapItemList"].append({
            "productSku": "YC7832-white-bag-s",
            "customerSku": "white-bag-s",
            "productName": "白色礼品袋",
            "productStatus": 1,
            "productStatusDescription": "正常",
            "quantity": 2,
            "imageUrl": (
                "https://example.com/bag.png"
            ),
        })

        result = map_bundle_record(source)

        self.assertEqual(
            len(result.items),
            2,
        )
        self.assertEqual(
            result.items[1].customer_sku,
            "white-bag-s",
        )
        self.assertEqual(
            result.items[1].required_quantity,
            3,
        )

    def test_missing_quantity_defaults_to_one(self):
        """子项未返回数量时默认按一件处理。"""

        source = self.create_source_record()

        source["mapItemList"][0].pop(
            "quantity"
        )

        result = map_bundle_record(source)

        self.assertEqual(
            result.items[0].required_quantity,
            1,
        )

    def test_missing_customer_sku_raises_error(self):
        """子项缺少客户SKU时拒绝转换。"""

        source = self.create_source_record()

        source["mapItemList"][0][
            "customerSku"
        ] = ""

        with self.assertRaises(
            CollectorResponseError
        ):
            map_bundle_record(source)

    def test_map_bundle_list_response(self):
        """可以转换元仓组合商品列表响应。"""

        source = {
            "state": "000001",
            "msg": "请求成功",
            "data": {
                "list": [
                    self.create_source_record()
                ],
                "total": 1,
                "page": 1,
                "prePage": 20,
            },
        }

        result = map_bundle_list_response(source)

        self.assertEqual(
            len(result),
            1,
        )
        self.assertEqual(
            result[0].bundle_sku,
            "SET-002-SUPER-1",
        )