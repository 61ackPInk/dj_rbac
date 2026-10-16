"""
-*- coding: utf-8 -*-
@File  : rbac_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 商品系统内置操作权限配置
"""


# ==================== 商品操作权限 ====================

PERMISSION_CONFIG = {
    "PRODUCT_LIST": [
        {
            "name": "查看商品列表",
            "code": "PRODUCT_LIST",
            "description": (
                "允许查看 ERP 商品列表及实时库存"
            ),
            "sort_order": 10,
        },
        {
            "name": "查看商品详情",
            "code": "PRODUCT_DETAIL",
            "description": (
                "允许查看指定商品的详细信息及实时库存"
            ),
            "sort_order": 20,
        },
    ],
    "PRODUCT_BUNDLE": [
        {
            "name": "查看组合商品列表",
            "code": "PRODUCT_BUNDLE_LIST",
            "description": (
                "允许查看组合商品列表及指定仓库的实时库存"
            ),
            "sort_order": 10,
        },
    ],
}
