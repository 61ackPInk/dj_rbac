"""
-*- coding: utf-8 -*-
@File  : test_bundle_operation_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表与详情接口操作权限测试
"""

from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.pages.models import Page
from apps.products.models import ProductBundle
from apps.products.services import BundleService
from apps.users.models import (
    Permission,
    Role,
    User,
)
from common.utils.jwt import create_access_token


class BundleOperationPermissionTests(TestCase):
    """组合商品列表与详情接口权限测试。"""

    def setUp(self):
        """创建组合页面、角色、权限和用户。"""

        self.client = APIClient()

        # ==================== 组合商品页面 ====================

        self.bundle_page = Page.objects.create(
            name="商品组合",
            code="PRODUCT_BUNDLE",
            path="/product/bundles",
            component="",
            icon="bi-boxes",
            sort_order=20,
            is_active=True,
        )

        # ==================== 测试角色 ====================

        self.role = Role.objects.create(
            name="组合商品测试角色",
            code="BUNDLE_TEST_ROLE",
            rank=500,
            description="测试组合商品接口权限",
            is_active=True,
        )

        self.bundle_page.visible_roles.add(
            self.role
        )

        # ==================== 操作权限 ====================

        self.list_permission = (
            Permission.objects.create(
                name="查看组合商品列表",
                code="PRODUCT_BUNDLE_LIST",
                page=self.bundle_page,
                sort_order=10,
                is_active=True,
            )
        )

        self.detail_permission = (
            Permission.objects.create(
                name="查看组合商品详情",
                code="PRODUCT_BUNDLE_DETAIL",
                page=self.bundle_page,
                sort_order=20,
                is_active=True,
            )
        )

        # ==================== 测试用户 ====================

        self.user = User.objects.create(
            username="bundle_operator",
            email="bundle@example.com",
            role=self.role,
            is_active=True,
            is_root=False,
        )
        self.user.set_password(
            "BundlePassword123!"
        )
        self.user.save(
            update_fields=["password"]
        )

        access_token = create_access_token(
            self.user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    # ==================== 模拟响应数据 ====================

    @staticmethod
    def create_bundle_result():
        """创建符合统一结构的组合列表响应。"""

        return {
            "items": [
                {
                    "id": 1,
                    "bundle_sku": "SET-001-A",
                    "name": "测试组合商品",
                    "image_url": "",
                    "source_status": "1",
                    "source_status_name": "启用",
                    "warehouse_code": "HK01",
                    "available_quantity": 10,
                    "item_count": 2,
                    "components": [
                        {
                            "provider_sku": (
                                "ERP-SKU-A"
                            ),
                            "customer_sku": (
                                "SKU-A"
                            ),
                            "name": "测试子商品A",
                            "image_url": "",
                            "required_quantity": 1,
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
                            "name": "测试子商品B",
                            "image_url": "",
                            "required_quantity": 1,
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

    @staticmethod
    def create_bundle_detail_result():
        """创建符合统一结构的组合详情响应。"""

        return {
            "id": 1,
            "bundle_sku": "SET-001-A",
            "name": "测试组合商品",
            "image_url": "",
            "source_status": "1",
            "source_status_name": "启用",
            "warehouse_code": "HK01",
            "available_quantity": 10,
            "item_count": 1,
            "components": [
                {
                    "provider_sku": (
                        "ERP-SKU-A"
                    ),
                    "customer_sku": "SKU-A",
                    "name": "测试子商品A",
                    "image_url": "",
                    "required_quantity": 2,
                    "available_quantity": 20,
                    "producible_quantity": 10,
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

    # ==================== 权限隔离测试 ====================

    def test_bundle_list_requires_operation_permission(
        self,
    ):
        """没有组合列表操作权限时应拒绝访问。"""

        response = self.client.get(
            "/api/products/bundles/",
            {
                "warehouse_code": "HK01",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_bundle_list_allows_authorized_user(
        self,
    ):
        """拥有组合列表操作权限时可以访问。"""

        self.role.permissions.add(
            self.list_permission
        )

        with (
            patch(
                "apps.products.views.bundles."
                "get_product_erp_provider_code",
                return_value="yuancang",
            ),
            patch(
                "apps.products.views.bundles."
                "get_stock_provider",
            ),
            patch.object(
                BundleService,
                "get_bundle_list",
                return_value=(
                    self.create_bundle_result()
                ),
            ),
        ):
            response = self.client.get(
                "/api/products/bundles/",
                {
                    "warehouse_code": "HK01",
                },
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items"][0][
                "available_quantity"
            ],
            10,
        )

    def test_bundle_list_requires_warehouse_code(
        self,
    ):
        """组合列表必须指定仓库编码。"""

        self.role.permissions.add(
            self.list_permission
        )

        response = self.client.get(
            "/api/products/bundles/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    # ==================== 详情权限隔离测试 ====================

    def test_bundle_detail_requires_detail_permission(
        self,
    ):
        """只有列表权限时不能访问组合详情。"""

        self.role.permissions.add(
            self.list_permission
        )

        response = self.client.get(
            "/api/products/bundles/1/",
            {
                "warehouse_code": "HK01",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_bundle_detail_allows_authorized_user(
        self,
    ):
        """拥有详情权限时可以查看组合详情。"""

        self.role.permissions.add(
            self.detail_permission
        )

        with (
            patch(
                "apps.products.views.bundles."
                "get_product_erp_provider_code",
                return_value="yuancang",
            ),
            patch(
                "apps.products.views.bundles."
                "get_stock_provider",
            ),
            patch.object(
                BundleService,
                "get_bundle_detail",
                return_value=(
                    self
                    .create_bundle_detail_result()
                ),
            ),
        ):
            response = self.client.get(
                "/api/products/bundles/1/",
                {
                    "warehouse_code": "HK01",
                },
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["components"][0][
                "available_quantity"
            ],
            20,
        )
        self.assertEqual(
            response.data["components"][0][
                "producible_quantity"
            ],
            10,
        )

    def test_bundle_detail_requires_warehouse_code(
        self,
    ):
        """组合详情必须提供仓库编码。"""

        self.role.permissions.add(
            self.detail_permission
        )

        response = self.client.get(
            "/api/products/bundles/1/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_bundle_detail_returns_not_found(
        self,
    ):
        """当前来源中不存在组合时返回404。"""

        self.role.permissions.add(
            self.detail_permission
        )

        with (
            patch(
                "apps.products.views.bundles."
                "get_product_erp_provider_code",
                return_value="yuancang",
            ),
            patch(
                "apps.products.views.bundles."
                "get_stock_provider",
            ),
            patch.object(
                BundleService,
                "get_bundle_detail",
                side_effect=(
                    ProductBundle.DoesNotExist
                ),
            ),
        ):
            response = self.client.get(
                "/api/products/bundles/999/",
                {
                    "warehouse_code": "HK01",
                },
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
