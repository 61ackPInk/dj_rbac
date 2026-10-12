"""
-*- coding: utf-8 -*-
@File  : test_product_operation_permissions.py
@Author: 61ackPink
@Time : 2026/10/12 11:02
@Desc : 商品接口操作权限隔离测试
"""

from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.pages.models import Page
from apps.products.services import ProductService
from apps.users.models import (
    Permission,
    Role,
    User,
)
from common.utils.jwt import create_access_token


class ProductOperationPermissionTests(TestCase):
    """商品列表与详情接口权限隔离测试。"""

    def setUp(self):
        """创建测试所需的页面、角色和用户。"""

        self.client = APIClient()

        # ====================
        # 创建商品列表页面
        # ====================

        self.product_page = Page.objects.create(
            name="商品列表",
            code="PRODUCT_LIST",
            path="/product/list",
            component="",
            icon="bi-box",
            sort_order=20,
            is_active=True,
        )

        # ====================
        # 创建商品测试角色
        # ====================

        self.product_role = Role.objects.create(
            name="商品测试角色",
            code="PRODUCT_TEST_ROLE",
            rank=500,
            description="测试商品接口权限",
            is_active=True,
        )

        # 角色必须先拥有商品列表页面，
        # 页面下的操作权限才能生效。
        self.product_page.visible_roles.add(
            self.product_role,
        )

        # ====================
        # 创建商品操作权限
        # ====================

        self.permissions = {}

        permission_data = [
            (
                "查看商品列表",
                "PRODUCT_LIST",
                10,
            ),
            (
                "查看商品详情",
                "PRODUCT_DETAIL",
                20,
            ),
        ]

        for name, code, sort_order in permission_data:
            permission = Permission.objects.create(
                name=name,
                code=code,
                page=self.product_page,
                sort_order=sort_order,
                is_active=True,
            )

            self.permissions[code] = permission

        # ====================
        # 创建并登录测试用户
        # ====================

        self.user = User.objects.create(
            username="product_operator",
            email="product@example.com",
            role=self.product_role,
            is_active=True,
            is_root=False,
        )

        self.user.set_password(
            "ProductPassword123!"
        )
        self.user.save(
            update_fields=[
                "password",
            ]
        )

        access_token = create_access_token(
            self.user,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=(
                f"Bearer {access_token}"
            )
        )

    # ====================
    # 权限分配辅助方法
    # ====================

    def grant_permissions(
        self,
        *permission_codes,
    ):
        """给商品测试角色分配指定权限。"""

        permissions = [
            self.permissions[code]
            for code in permission_codes
        ]

        self.product_role.permissions.add(
            *permissions,
        )

    # ====================
    # 商品详情响应数据
    # ====================

    @staticmethod
    def create_product_detail():
        """创建符合统一序列化结构的商品详情。"""

        return {
            "id": "1",
            "customer_sku": "SET-001",
            "erp_sku": "ERP-SET-001",
            "name": "测试商品",
            "english_name": "Test Product",
            "reference_code": None,
            "category_id": None,
            "status": 1,
            "status_name": "正常",
            "product_type": 1,
            "product_type_name": "普通商品",
            "unit_code": "PCS",
            "unit_name": "件",
            "main_warehouse": {
                "code": "US",
                "name": "美国仓",
            },
            "images": [],
            "specifications": {
                "length": None,
                "width": None,
                "height": None,
                "weight": None,
                "package_length": None,
                "package_width": None,
                "package_height": None,
                "package_weight": None,
            },
            "inventory": {
                "found": True,
                "warehouse_code": "US",
                "site_code": None,
                "preparing": 0,
                "transferring": 0,
                "waiting_for_shelf": 0,
                "total": 100,
                "occupied": 20,
                "unshipped": 5,
                "available": 75,
                "status_name": "正常",
                "lock_status_name": "未锁定",
            },
            "created_at": None,
            "updated_at": None,
            "declared_name": None,
            "declared_chinese_name": None,
            "product_link": None,
            "product_attribute": None,
            "product_attribute_name": None,
            "has_brand": False,
            "brand_name": None,
            "model": None,
            "usage": None,
            "material": None,
            "reference_cost_price": None,
            "inbound_customs": [],
            "outbound_customs": None,
            "warehouses": [],
        }

    # ====================
    # 商品列表权限测试
    # ====================

    def test_product_list_permission_isolated(self):
        """
        PRODUCT_LIST 可以访问商品列表，
        但不能访问商品详情。
        """

        self.grant_permissions(
            "PRODUCT_LIST",
        )

        list_result = {
            "items": [],
            "pagination": {
                "page": 1,
                "page_size": 20,
                "total": 0,
            },
        }

        with (
            patch(
                "apps.products.views.products."
                "get_product_provider"
            ),
            patch(
                "apps.products.views.products."
                "get_stock_provider"
            ),
            patch.object(
                ProductService,
                "get_product_list",
                return_value=list_result,
            ),
        ):
            list_response = self.client.get(
                "/api/products/",
            )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_200_OK,
        )

        detail_response = self.client.get(
            "/api/products/by-sku/SET-001/",
        )

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ====================
    # 商品详情权限测试
    # ====================

    def test_product_detail_permission_isolated(self):
        """
        PRODUCT_DETAIL 可以访问商品详情，
        但不能访问商品列表。
        """

        self.grant_permissions(
            "PRODUCT_DETAIL",
        )

        detail_result = (
            self.create_product_detail()
        )

        with (
            patch(
                "apps.products.views.products."
                "get_product_provider"
            ),
            patch(
                "apps.products.views.products."
                "get_stock_provider"
            ),
            patch.object(
                ProductService,
                "get_product_detail",
                return_value=detail_result,
            ),
        ):
            detail_response = self.client.get(
                "/api/products/by-sku/SET-001/",
            )

        self.assertEqual(
            detail_response.status_code,
            status.HTTP_200_OK,
        )

        list_response = self.client.get(
            "/api/products/",
        )

        self.assertEqual(
            list_response.status_code,
            status.HTTP_403_FORBIDDEN,
        )