"""
-*- coding: utf-8 -*-
@File  : warehouses.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 客户已开启仓库响应序列化器
"""

from rest_framework import serializers


# ==================== 仓库列表项 ====================


class WarehouseListItemSerializer(
    serializers.Serializer
):
    """统一仓库列表项响应结构。"""

    id = serializers.CharField(
        allow_null=True,
    )

    code = serializers.CharField(
        allow_blank=False,
    )

    name = serializers.CharField(
        allow_blank=False,
    )

    site_code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    address = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    contact_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    contact_phone = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )


# ==================== 仓库列表响应 ====================


class WarehouseListResponseSerializer(
    serializers.Serializer
):
    """统一仓库列表响应结构。"""

    items = WarehouseListItemSerializer(
        many=True,
    )