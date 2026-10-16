"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表查询参数与响应序列化器
"""

from rest_framework import serializers


# ==================== 组合列表查询参数 ====================


class BundleListQuerySerializer(
    serializers.Serializer
):
    """校验组合商品列表查询参数。"""

    warehouse_code = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "required": "仓库编码不能为空",
            "blank": "仓库编码不能为空",
        },
    )

    page = serializers.IntegerField(
        required=False,
        default=1,
        min_value=1,
        error_messages={
            "invalid": "页码必须是整数",
            "min_value": "页码必须大于0",
        },
    )

    page_size = serializers.IntegerField(
        required=False,
        default=20,
        min_value=1,
        max_value=100,
        error_messages={
            "invalid": "每页数量必须是整数",
            "min_value": "每页数量必须大于0",
            "max_value": "每页数量不能超过100",
        },
    )

    bundle_sku = serializers.CharField(
        required=False,
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "blank": "组合SKU不能为空",
        },
    )

    name = serializers.CharField(
        required=False,
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "blank": "组合名称不能为空",
        },
    )

    # ==================== 服务层查询参数 ====================

    def to_service_query(self) -> dict:
        """返回组合商品服务使用的查询参数。"""

        return dict(self.validated_data)


# ==================== 组合组成明细 ====================

class BundleComponentSerializer(
    serializers.Serializer
):
    """组合商品中的一个组成商品。"""

    provider_sku = serializers.CharField(
        allow_blank=True,
    )

    customer_sku = serializers.CharField(
        allow_blank=False,
    )

    name = serializers.CharField(
        allow_blank=True,
    )

    image_url = serializers.URLField(
        allow_blank=True,
    )

    required_quantity = serializers.IntegerField(
        min_value=1,
    )

    source_status = serializers.CharField(
        allow_blank=True,
    )

    source_status_name = serializers.CharField(
        allow_blank=True,
    )


# ==================== 组合列表项 ====================


class BundleListItemSerializer(
    serializers.Serializer
):
    """组合商品列表项统一响应结构。"""

    id = serializers.IntegerField()

    bundle_sku = serializers.CharField(
        allow_blank=False,
    )

    name = serializers.CharField(
        allow_blank=True,
    )

    image_url = serializers.URLField(
        allow_blank=True,
    )

    source_status = serializers.CharField(
        allow_blank=True,
    )

    source_status_name = serializers.CharField(
        allow_blank=True,
    )

    warehouse_code = serializers.CharField(
        allow_blank=False,
    )

    available_quantity = serializers.IntegerField(
        min_value=0,
    )

    item_count = serializers.IntegerField(
        min_value=0,
    )

    components = BundleComponentSerializer(
        many=True,
    )

    collected_at = serializers.DateTimeField()


# ==================== 组合分页信息 ====================


class BundlePaginationSerializer(
    serializers.Serializer
):
    """组合商品列表分页响应结构。"""

    page = serializers.IntegerField(
        min_value=1,
    )

    page_size = serializers.IntegerField(
        min_value=1,
    )

    total = serializers.IntegerField(
        min_value=0,
    )


# ==================== 组合列表响应 ====================


class BundleListResponseSerializer(
    serializers.Serializer
):
    """组合商品列表统一响应结构。"""

    items = BundleListItemSerializer(
        many=True,
    )

    pagination = BundlePaginationSerializer()