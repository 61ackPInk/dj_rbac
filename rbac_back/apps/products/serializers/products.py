"""
-*- coding: utf-8 -*-
@File  : products.py
@Author: 61ackPink
@Time : 2026/10/10 17:12
@Desc : 普通商品查询参数与列表响应序列化器
"""

from rest_framework import serializers


# ==================== 商品详情路径参数 ====================


class ProductDetailPathSerializer(
    serializers.Serializer
):
    """校验商品详情中的客户SKU。"""

    customer_sku = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "blank": "客户SKU不能为空",
        },
    )


# ==================== 商品列表查询参数 ====================


class ProductListQuerySerializer(
    serializers.Serializer
):
    """校验本系统商品列表查询参数。"""

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

    customer_sku = serializers.CharField(
        required=False,
        allow_blank=False,
        trim_whitespace=True,
        error_messages={
            "blank": "客户SKU不能为空",
        },
    )

    category_id = serializers.IntegerField(
        required=False,
        min_value=1,
        error_messages={
            "invalid": "商品分类ID必须是整数",
            "min_value": "商品分类ID必须大于0",
        },
    )

    created_at_from = serializers.DateTimeField(
        required=False,
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
        ],
        error_messages={
            "invalid": (
                "开始时间格式必须为"
                "YYYY-MM-DD HH:MM:SS"
            ),
        },
    )

    created_at_to = serializers.DateTimeField(
        required=False,
        input_formats=[
            "%Y-%m-%d %H:%M:%S",
        ],
        error_messages={
            "invalid": (
                "结束时间格式必须为"
                "YYYY-MM-DD HH:MM:SS"
            ),
        },
    )

    # ==================== 时间范围校验 ====================

    def validate(self, attrs):
        """确保开始时间不晚于结束时间。"""

        created_at_from = attrs.get(
            "created_at_from"
        )
        created_at_to = attrs.get(
            "created_at_to"
        )

        if (
                created_at_from
                and created_at_to
                and created_at_from
                > created_at_to
        ):
            raise serializers.ValidationError({
                "created_at_to": (
                    "结束时间不能早于开始时间"
                ),
            })

        return attrs

    # ==================== 服务层查询参数 ====================

    def to_service_query(self):
        """
        返回服务层需要的查询字典。

        DateTimeField 验证后会生成 datetime，
        调用元仓前需要重新转换为接口要求的字符串。
        """

        query = dict(self.validated_data)

        for field_name in [
            "created_at_from",
            "created_at_to",
        ]:
            value = query.get(field_name)

            if value:
                query[field_name] = (
                    value.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )

        return query


# ==================== 商品仓库信息 ====================


class ProductMainWarehouseSerializer(
    serializers.Serializer
):
    """商品主仓库响应结构。"""

    code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )


# ==================== 商品规格信息 ====================


class ProductSpecificationsSerializer(
    serializers.Serializer
):
    """商品及包装尺寸响应结构。"""

    length = serializers.FloatField(
        allow_null=True
    )
    width = serializers.FloatField(
        allow_null=True
    )
    height = serializers.FloatField(
        allow_null=True
    )
    weight = serializers.FloatField(
        allow_null=True
    )
    package_length = serializers.FloatField(
        allow_null=True
    )
    package_width = serializers.FloatField(
        allow_null=True
    )
    package_height = serializers.FloatField(
        allow_null=True
    )
    package_weight = serializers.FloatField(
        allow_null=True
    )


# ==================== 商品库存信息 ====================


class ProductInventorySerializer(
    serializers.Serializer
):
    """统一商品实时库存结构。"""

    found = serializers.BooleanField()

    warehouse_code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    site_code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    preparing = serializers.IntegerField(
        allow_null=True
    )
    transferring = serializers.IntegerField(
        allow_null=True
    )
    waiting_for_shelf = serializers.IntegerField(
        allow_null=True
    )
    total = serializers.IntegerField(
        allow_null=True
    )
    occupied = serializers.IntegerField(
        allow_null=True
    )
    unshipped = serializers.IntegerField(
        allow_null=True
    )
    available = serializers.IntegerField(
        allow_null=True
    )

    status_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    lock_status_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )


# ==================== 商品列表项 ====================


class ProductListItemSerializer(
    serializers.Serializer
):
    """本系统统一商品列表项。"""

    id = serializers.CharField(
        allow_null=True
    )
    customer_sku = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    erp_sku = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    english_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    reference_code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    category_id = serializers.CharField(
        allow_null=True
    )
    status = serializers.IntegerField(
        allow_null=True
    )
    status_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    product_type = serializers.IntegerField(
        allow_null=True
    )
    product_type_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    unit_code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    unit_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    main_warehouse = (
        ProductMainWarehouseSerializer()
    )

    images = serializers.ListField(
        child=serializers.CharField(),
    )

    specifications = (
        ProductSpecificationsSerializer()
    )

    inventory = ProductInventorySerializer()

    created_at = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    updated_at = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )


# ==================== 商品报关信息 ====================


class ProductCustomsSerializer(
    serializers.Serializer
):
    """商品报关国家和价格信息。"""

    country = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    price = serializers.FloatField(
        allow_null=True
    )


# ==================== 商品仓库价格信息 ====================


class ProductWarehouseInfoSerializer(
    serializers.Serializer
):
    """商品在仓库中的价格信息。"""

    code = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    purchase_price = serializers.FloatField(
        allow_null=True
    )
    stock_price = serializers.FloatField(
        allow_null=True
    )
    updated_at = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )


# ==================== 商品详情响应 ====================


class ProductDetailSerializer(
    ProductListItemSerializer
):
    """本系统统一商品详情结构。"""

    declared_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    declared_chinese_name = (
        serializers.CharField(
            allow_blank=True,
            allow_null=True,
        )
    )
    product_link = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )

    product_attribute = (
        serializers.IntegerField(
            allow_null=True
        )
    )
    product_attribute_name = (
        serializers.CharField(
            allow_blank=True,
            allow_null=True,
        )
    )

    has_brand = serializers.BooleanField()

    brand_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    model = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    usage = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    material = serializers.CharField(
        allow_blank=True,
        allow_null=True,
    )
    reference_cost_price = (
        serializers.CharField(
            allow_blank=True,
            allow_null=True,
        )
    )

    inbound_customs = (
        ProductCustomsSerializer(
            many=True
        )
    )
    outbound_customs = (
        ProductCustomsSerializer(
            allow_null=True
        )
    )
    warehouses = (
        ProductWarehouseInfoSerializer(
            many=True
        )
    )


# ==================== 商品分页信息 ====================


class ProductPaginationSerializer(
    serializers.Serializer
):
    """统一商品分页响应结构。"""

    page = serializers.IntegerField(
        allow_null=True
    )
    page_size = serializers.IntegerField(
        allow_null=True
    )
    total = serializers.IntegerField(
        allow_null=True
    )


# ==================== 商品列表响应 ====================


class ProductListResponseSerializer(
    serializers.Serializer
):
    """统一商品列表响应结构。"""

    items = ProductListItemSerializer(
        many=True
    )
    pagination = ProductPaginationSerializer()
