"""
-*- coding: utf-8 -*-
@File  : test_yuancang_warehouse_provider.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓客户仓库适配器测试
"""

from unittest.mock import Mock

from django.test import SimpleTestCase

from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)
from apps.products.adapters.yuancang.warehouses.endpoints import (
    YUANCANG_CUSTOMER_WAREHOUSE_PATH,
)
from apps.products.adapters.yuancang.warehouses.provider import (
    YuanCangWarehouseProvider,
)


class YuanCangWarehouseProviderTests(
    SimpleTestCase
):
    """元仓客户仓库适配器测试。"""

    def setUp(self):
        """初始化模拟客户端和仓库适配器。"""

        self.client = Mock()
        self.provider = (
            YuanCangWarehouseProvider(
                client=self.client
            )
        )

    # ==================== 仓库字段转换 ====================

    def test_get_warehouse_list_maps_response(
        self,
    ):
        """元仓仓库数据应转换为统一结构。"""

        self.client.post.return_value = [
            {
                "id": 1001,
                "code": "US",
                "name": "美国仓",
                "siteCode": "US-SITE",
                "address": "测试地址",
                "contacts": "测试联系人",
                "phone": "123456",
            }
        ]

        result = (
            self.provider
            .get_warehouse_list()
        )

        self.client.post.assert_called_once_with(
            YUANCANG_CUSTOMER_WAREHOUSE_PATH,
            {},
        )

        self.assertEqual(
            result,
            [
                {
                    "id": "1001",
                    "code": "US",
                    "name": "美国仓",
                    "site_code": "US-SITE",
                    "address": "测试地址",
                    "contact_name": "测试联系人",
                    "contact_phone": "123456",
                }
            ],
        )

    def test_get_warehouse_list_rejects_invalid_data(
        self,
    ):
        """元仓仓库响应不是列表时应拒绝处理。"""

        self.client.post.return_value = {
            "code": "US",
        }

        with self.assertRaisesMessage(
            ProductProviderResponseError,
            "元仓客户仓库响应 data 必须是列表",
        ):
            self.provider.get_warehouse_list()