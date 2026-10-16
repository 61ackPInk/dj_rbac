"""
-*- coding: utf-8 -*-
@File  : __init__.py.py
@Author: 61ackPink
@Time : 2026/10/10 17:12
@Desc : 商品系统序列化器统一导出
"""

from .products import (
    ProductInventorySerializer,
    ProductListItemSerializer,
    ProductListQuerySerializer,
    ProductListResponseSerializer,
    ProductMainWarehouseSerializer,
    ProductPaginationSerializer,
    ProductSpecificationsSerializer,
    ProductCustomsSerializer,
    ProductDetailPathSerializer,
    ProductDetailSerializer,
    ProductWarehouseInfoSerializer,
)

from .bundles import (
    BundleListItemSerializer,
    BundleListQuerySerializer,
    BundleListResponseSerializer,
    BundlePaginationSerializer,
    BundleComponentSerializer,
)

from .warehouses import (
    WarehouseListItemSerializer,
    WarehouseListResponseSerializer,
)

__all__ = [
    "ProductInventorySerializer",
    "ProductListItemSerializer",
    "ProductListQuerySerializer",
    "ProductListResponseSerializer",
    "ProductMainWarehouseSerializer",
    "ProductPaginationSerializer",
    "ProductSpecificationsSerializer",
    "ProductCustomsSerializer",
    "ProductDetailPathSerializer",
    "ProductDetailSerializer",
    "ProductWarehouseInfoSerializer",

    # 商品组合
    "BundleListItemSerializer",
    "BundleListQuerySerializer",
    "BundleListResponseSerializer",
    "BundlePaginationSerializer",
    "BundleComponentSerializer",

    # 仓库
    "WarehouseListItemSerializer",
    "WarehouseListResponseSerializer",
]
