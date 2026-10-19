"""
-*- coding: utf-8 -*-
@File  : test_warehouse_serializers.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 客户仓库响应序列化器测试
"""

from django.test import SimpleTestCase

from apps.products.serializers import (
    WarehouseListResponseSerializer,
)


class WarehouseSerializerTests(
    SimpleTestCase
):
    """客户仓库响应序列化器测试。"""

    def test_accepts_warehouse_list(self):
        """合法仓库列表应通过响应校验。"""

        serializer = (
            WarehouseListResponseSerializer(
                data={
                    "items": [
                        {
                            "id": "1",
                            "code": "US",
                            "name": "美国仓",
                            "site_code": "US-SITE",
                            "address": "",
                            "contact_name": "",
                            "contact_phone": "",
                        }
                    ],
                }
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_rejects_missing_warehouse_code(
        self,
    ):
        """仓库编码缺失时应拒绝响应。"""

        serializer = (
            WarehouseListResponseSerializer(
                data={
                    "items": [
                        {
                            "id": "1",
                            "name": "美国仓",
                            "site_code": None,
                            "address": None,
                            "contact_name": None,
                            "contact_phone": None,
                        }
                    ],
                }
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )