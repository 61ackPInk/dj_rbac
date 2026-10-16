"""
-*- coding: utf-8 -*-
@File  : test_warehouse_service.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 客户仓库业务服务测试
"""

from unittest.mock import Mock

from django.test import SimpleTestCase

from apps.products.adapters import (
    BaseWarehouseProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)
from apps.products.services import WarehouseService


class WarehouseServiceTests(SimpleTestCase):
    """客户仓库业务服务测试。"""

    def setUp(self):
        """初始化模拟仓库 Provider。"""

        self.provider = Mock(
            spec=BaseWarehouseProvider
        )
        self.service = WarehouseService(
            warehouse_provider=self.provider
        )

    def test_returns_warehouse_items(self):
        """仓库服务应返回统一列表结构。"""

        warehouses = [
            {
                "id": "1",
                "code": "US",
                "name": "美国仓",
                "site_code": "US-SITE",
                "address": "",
                "contact_name": "",
                "contact_phone": "",
            }
        ]

        self.provider.get_warehouse_list.return_value = (
            warehouses
        )

        result = (
            self.service.get_warehouse_list()
        )

        self.assertEqual(
            result,
            {
                "items": warehouses,
            },
        )

    def test_rejects_invalid_provider_result(self):
        """仓库 Provider 返回非列表时应拒绝处理。"""

        self.provider.get_warehouse_list.return_value = {
            "code": "US",
        }

        with self.assertRaisesMessage(
            ProductProviderResponseError,
            "仓库 Provider 返回格式错误",
        ):
            self.service.get_warehouse_list()