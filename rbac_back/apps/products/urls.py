"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/10/10 17:16
@Desc : 商品系统接口路由
"""

from django.urls import path

from apps.products.views import (
    ProductDetailAPIView,
    ProductListAPIView,
    BundleListAPIView,
    WarehouseListAPIView,
)


# ==================== 商品系统路由 ====================

urlpatterns = [
    # 普通商品列表
    path(
        "",
        ProductListAPIView.as_view(),
        name="product-list",
    ),
    # 普通商品详情
    path(
        "by-sku/<str:customer_sku>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    # 组合商品列表
    path(
        "bundles/",
        BundleListAPIView.as_view(),
        name="bundle-list",
    ),
    # 客户已开启仓库列表
    path(
        "warehouses/",
        WarehouseListAPIView.as_view(),
        name="warehouse-list",
    ),
]