"""
-*- coding: utf-8 -*-
@File  : test_bundle_serializers.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表序列化器测试
"""

from django.test import SimpleTestCase

from apps.products.serializers import (
    BundleDetailPathSerializer,
    BundleDetailQuerySerializer,
    BundleDetailResponseSerializer,
    BundleListQuerySerializer,
    BundleListResponseSerializer,
)


class BundleListSerializerTests(
    SimpleTestCase
):
    """组合商品列表序列化器测试。"""

    # ==================== 详情路径参数校验 ====================

    def test_detail_path_accepts_positive_id(
        self,
    ):
        """正整数可以作为组合详情ID。"""

        serializer = (
            BundleDetailPathSerializer(
                data={
                    "bundle_id": 1,
                }
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data[
                "bundle_id"
            ],
            1,
        )

    def test_detail_path_rejects_zero_id(
        self,
    ):
        """组合详情ID必须大于0。"""

        serializer = (
            BundleDetailPathSerializer(
                data={
                    "bundle_id": 0,
                }
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "bundle_id",
            serializer.errors,
        )

    # ==================== 详情查询参数校验 ====================

    def test_detail_query_accepts_warehouse_code(
        self,
    ):
        """详情查询应清理仓库编码两侧空格。"""

        serializer = (
            BundleDetailQuerySerializer(
                data={
                    "warehouse_code": " 055 ",
                }
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.to_service_query(),
            {
                "warehouse_code": "055",
            },
        )

    def test_detail_query_requires_warehouse_code(
        self,
    ):
        """组合详情必须提供仓库编码。"""

        serializer = (
            BundleDetailQuerySerializer(
                data={}
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "warehouse_code",
            serializer.errors,
        )

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

    def test_response_accepts_bundle_detail(
        self,
    ):
        """合法的组合详情响应应通过校验。"""

        serializer = (
            BundleDetailResponseSerializer(
                data={
                    "id": 1,
                    "bundle_sku": (
                        "SET-001-A"
                    ),
                    "name": "组合商品A",
                    "image_url": "",
                    "source_status": "1",
                    "source_status_name": (
                        "启用"
                    ),
                    "warehouse_code": "055",
                    "available_quantity": 12,
                    "item_count": 2,
                    "components": [
                        {
                            "provider_sku": (
                                "ERP-SKU-A"
                            ),
                            "customer_sku": (
                                "SKU-A"
                            ),
                            "name": "子商品A",
                            "image_url": "",
                            "required_quantity": 1,
                            "available_quantity": 20,
                            "producible_quantity": 20,
                            "source_status": "1",
                            "source_status_name": (
                                "正常"
                            ),
                        },
                        {
                            "provider_sku": (
                                "ERP-SKU-B"
                            ),
                            "customer_sku": (
                                "SKU-B"
                            ),
                            "name": "子商品B",
                            "image_url": "",
                            "required_quantity": 2,
                            "available_quantity": 25,
                            "producible_quantity": 12,
                            "source_status": "1",
                            "source_status_name": (
                                "正常"
                            ),
                        },
                    ],
                    "collected_at": (
                        "2026-10-18T10:00:00"
                        "+08:00"
                    ),
                }
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_detail_rejects_missing_component_stock(
        self,
    ):
        """详情组成商品缺少实时库存时应校验失败。"""

        serializer = (
            BundleDetailResponseSerializer(
                data={
                    "id": 1,
                    "bundle_sku": (
                        "SET-001-A"
                    ),
                    "name": "组合商品A",
                    "image_url": "",
                    "source_status": "1",
                    "source_status_name": (
                        "启用"
                    ),
                    "warehouse_code": "055",
                    "available_quantity": 0,
                    "item_count": 1,
                    "components": [
                        {
                            "provider_sku": (
                                "ERP-SKU-A"
                            ),
                            "customer_sku": (
                                "SKU-A"
                            ),
                            "name": "子商品A",
                            "image_url": "",
                            "required_quantity": 1,
                            "source_status": "1",
                            "source_status_name": (
                                "正常"
                            ),
                        }
                    ],
                    "collected_at": (
                        "2026-10-18T10:00:00"
                        "+08:00"
                    ),
                }
            )
        )

        self.assertFalse(
            serializer.is_valid()
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
