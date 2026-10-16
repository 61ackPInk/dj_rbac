"""
-*- coding: utf-8 -*-
@File  : test_warehouse_operation_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 共享仓库列表接口操作权限测试
"""

from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.pages.models import Page
from apps.products.services import (
    WarehouseService,
)
from apps.users.models import (
    Permission,
    Role,
    User,
)
from common.utils.jwt import create_access_token


class WarehouseOperationPermissionTests(
    TestCase
):
    """共享仓库列表接口权限测试。"""

    def setUp(self):
        """创建商品页面、权限、角色和用户。"""

        self.client = APIClient()

        # ==================== 商品页面 ====================

        self.product_page = Page.objects.create(
            name="商品列表",
            code="PRODUCT_LIST",
            path="/product/list",
            component="",
            icon="bi-box",
            sort_order=20,
            is_active=True,
        )

        self.bundle_page = Page.objects.create(
            name="商品组合",
            code="PRODUCT_BUNDLE",
            path="/product/bundles",
            component="",
            icon="bi-boxes",
            sort_order=30,
            is_active=True,
        )

        # ==================== 测试角色 ====================

        self.role = Role.objects.create(
            name="仓库接口测试角色",
            code="WAREHOUSE_TEST_ROLE",
            rank=500,
            description="测试共享仓库接口权限",
            is_active=True,
        )

        # ==================== 操作权限 ====================

        self.product_list_permission = (
            Permission.objects.create(
                name="查看商品列表",
                code="PRODUCT_LIST",
                page=self.product_page,
                sort_order=10,
                is_active=True,
            )
        )

        self.bundle_list_permission = (
            Permission.objects.create(
                name="查看组合商品列表",
                code="PRODUCT_BUNDLE_LIST",
                page=self.bundle_page,
                sort_order=10,
                is_active=True,
            )
        )

        # ==================== 测试用户 ====================

        self.user = User.objects.create(
            username="warehouse_operator",
            email="warehouse@example.com",
            role=self.role,
            is_active=True,
            is_root=False,
        )

        self.user.set_password(
            "WarehousePassword123!"
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

    # ==================== 模拟仓库数据 ====================

    @staticmethod
    def create_warehouse_result():
        """创建符合统一结构的仓库列表响应。"""

        return {
            "items": [
                {
                    "id": "1",
                    "code": "HK01",
                    "name": "香港仓",
                    "site_code": "HK",
                    "address": "香港",
                    "contact_name": "",
                    "contact_phone": "",
                }
            ],
        }

    # ==================== 接口调用辅助方法 ====================

    def request_warehouse_list(self):
        """模拟业务服务并请求仓库列表。"""

        with (
            patch(
                "apps.products.views.warehouses."
                "get_warehouse_provider"
            ),
            patch.object(
                WarehouseService,
                "get_warehouse_list",
                return_value=(
                    self.create_warehouse_result()
                ),
            ),
        ):
            return self.client.get(
                "/api/products/warehouses/",
            )

    # ==================== 无权限测试 ====================

    def test_warehouse_list_denies_user_without_permission(
        self,
    ):
        """没有候选权限时应拒绝访问。"""

        response = (
            self.request_warehouse_list()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ==================== 商品列表权限测试 ====================

    def test_product_list_permission_allows_access(
        self,
    ):
        """PRODUCT_LIST 可以访问共享仓库接口。"""

        # 操作权限所属页面也必须分配给角色
        self.product_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.product_list_permission,
        )

        response = (
            self.request_warehouse_list()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items"][0]["code"],
            "HK01",
        )

    # ==================== 商品组合权限测试 ====================

    def test_bundle_list_permission_allows_access(
        self,
    ):
        """
        PRODUCT_BUNDLE_LIST
        可以访问共享仓库接口。
        """

        # 操作权限所属页面也必须分配给角色
        self.bundle_page.visible_roles.add(
            self.role,
        )

        self.role.permissions.add(
            self.bundle_list_permission,
        )

        response = (
            self.request_warehouse_list()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["items"][0]["name"],
            "香港仓",
        )

    # ==================== 页面权限测试 ====================

    def test_permission_without_page_is_denied(
        self,
    ):
        """只有操作权限而没有页面时应拒绝访问。"""

        self.role.permissions.add(
            self.product_list_permission,
        )

        response = (
            self.request_warehouse_list()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )