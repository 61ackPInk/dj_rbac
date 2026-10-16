"""
-*- coding: utf-8 -*-
@File  : test_bundle_serializers.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表序列化器测试
"""

from django.test import SimpleTestCase

from apps.products.serializers import (
    BundleListQuerySerializer,
    BundleListResponseSerializer,
)


class BundleListSerializerTests(
    SimpleTestCase
):
    """组合商品列表序列化器测试。"""

    # ==================== 查询参数校验 ====================

    def test_query_uses_default_pagination(self):
        """只提交仓库编码时应使用默认分页。"""

        serializer = BundleListQuerySerializer(
            data={
                "warehouse_code": " HK01 ",
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.to_service_query(),
            {
                "warehouse_code": "HK01",
                "page": 1,
                "page_size": 20,
            },
        )

    def test_query_requires_warehouse_code(self):
        """组合列表必须指定仓库编码。"""

        serializer = BundleListQuerySerializer(
            data={}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "warehouse_code",
            serializer.errors,
        )

    def test_query_rejects_oversized_page(self):
        """每页数量不能超过100。"""

        serializer = BundleListQuerySerializer(
            data={
                "warehouse_code": "HK01",
                "page_size": 101,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "page_size",
            serializer.errors,
        )

    # ==================== 响应结构校验 ====================

    def test_response_accepts_bundle_list(self):
        """合法的组合列表响应应通过校验。"""

        serializer = BundleListResponseSerializer(
            data={
                "items": [
                    {
                        "id": 1,
                        "bundle_sku": "SET-001-A",
                        "name": "组合商品A",
                        "image_url": "",
                        "source_status": "1",
                        "source_status_name": "启用",
                        "warehouse_code": "HK01",
                        "available_quantity": 75,
                        "item_count": 2,
                        "components": [
                            {
                                "provider_sku": (
                                    "YC7832-SET-001"
                                ),
                                "customer_sku": (
                                    "SET-001"
                                ),
                                "name": "咖啡杯",
                                "image_url": "",
                                "required_quantity": 1,
                                "source_status": "1",
                                "source_status_name": (
                                    "正常"
                                ),
                            },
                            {
                                "provider_sku": (
                                    "YC7832-ARO-001"
                                ),
                                "customer_sku": (
                                    "ARO-001"
                                ),
                                "name": "香薰",
                                "image_url": "",
                                "required_quantity": 2,
                                "source_status": "1",
                                "source_status_name": (
                                    "正常"
                                ),
                            },
                        ],
                        "collected_at": (
                            "2026-10-16T18:00:00"
                            "+08:00"
                        ),
                    }
                ],
                "pagination": {
                    "page": 1,
                    "page_size": 20,
                    "total": 1,
                },
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )