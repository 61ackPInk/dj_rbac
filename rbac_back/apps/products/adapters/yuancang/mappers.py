"""
-*- coding: utf-8 -*-
@File  : mappers.py
@Author: 61ackPink
@Time : 2026/10/10 17:05
@Desc : 元仓商品字段与统一商品结构转换
"""

from typing import Any


# ==================== 基础字段转换 ====================


def _string_id(value: Any) -> str | None:
    """将不同 ERP 的标识统一转换为字符串。"""

    if value is None:
        return None

    return str(value)


def _map_product_specs(
    source: Any,
) -> dict[str, Any]:
    """转换商品及包装尺寸信息。"""

    if not isinstance(source, dict):
        source = {}

    return {
        "length": source.get("length"),
        "width": source.get("width"),
        "height": source.get("height"),
        "weight": source.get("weigh"),
        "package_length": source.get(
            "packageLength"
        ),
        "package_width": source.get(
            "packageWidth"
        ),
        "package_height": source.get(
            "packageHeight"
        ),
        "package_weight": source.get(
            "packageWeigh"
        ),
    }


def _map_main_warehouse(
    source: dict[str, Any],
) -> dict[str, Any]:
    """转换商品主仓库信息。"""

    return {
        "code": source.get(
            "mainWarehouseCode"
        ),
        "name": source.get(
            "mainWarehouseName"
        ),
    }


# ==================== 商品公共字段 ====================


def map_product_common(
    source: dict[str, Any],
) -> dict[str, Any]:
    """转换商品列表和详情共用字段。"""

    images = source.get("productImages")

    if not isinstance(images, list):
        images = []

    return {
        "id": _string_id(
            source.get("id")
        ),
        "customer_sku": source.get(
            "customerSku"
        ),
        "erp_sku": source.get(
            "productSku"
        ),
        "name": source.get(
            "productCnName"
        ),
        "english_name": source.get(
            "productName"
        ),
        "reference_code": source.get(
            "productRefCode"
        ),
        "category_id": _string_id(
            source.get("categoryId")
        ),
        "status": source.get("status"),
        "status_name": source.get(
            "statusDescription"
        ),
        "product_type": source.get(
            "productType"
        ),
        "product_type_name": source.get(
            "productTypeDescription"
        ),
        "unit_code": source.get(
            "unitCode"
        ),
        "unit_name": source.get("unit"),
        "main_warehouse": (
            _map_main_warehouse(source)
        ),
        "images": images,
        "specifications": (
            _map_product_specs(
                source.get("productSpecs")
            )
        ),
        "created_at": source.get(
            "createTime"
        ),
        "updated_at": source.get(
            "updateTime"
        ),
    }


# ==================== 商品列表字段 ====================


def map_product_list_item(
    source: dict[str, Any],
) -> dict[str, Any]:
    """将元仓商品列表项转换为统一结构。"""

    return map_product_common(source)


# ==================== 商品详情扩展字段 ====================


def _map_customs_items(
    source: Any,
) -> list[dict[str, Any]]:
    """转换多条报关信息。"""

    if not isinstance(source, list):
        return []

    return [
        {
            "country": item.get("country"),
            "price": item.get("price"),
        }
        for item in source
        if isinstance(item, dict)
    ]


def _map_outbound_customs(
    source: Any,
) -> dict[str, Any] | None:
    """转换出口报关信息。"""

    if not isinstance(source, dict):
        return None

    return {
        "country": source.get("country"),
        "price": source.get("price"),
    }


def _map_warehouse_items(
    source: Any,
) -> list[dict[str, Any]]:
    """转换商品仓库价格信息。"""

    if not isinstance(source, list):
        return []

    return [
        {
            "code": item.get(
                "warehouseCode"
            ),
            "name": item.get(
                "warehouseName"
            ),
            "purchase_price": item.get(
                "purchasePrice"
            ),
            "stock_price": item.get(
                "stockPrice"
            ),
            "updated_at": item.get(
                "updatedAt"
            ),
        }
        for item in source
        if isinstance(item, dict)
    ]


def map_product_detail(
    source: dict[str, Any],
) -> dict[str, Any]:
    """将元仓商品详情转换为统一结构。"""

    product = map_product_common(source)

    product.update({
        "declared_name": source.get(
            "productDeclareName"
        ),
        "declared_chinese_name": source.get(
            "productDeclareCnName"
        ),
        "product_link": source.get(
            "productLink"
        ),
        "product_attribute": source.get(
            "productAttr"
        ),
        "product_attribute_name": source.get(
            "productAttrDescription"
        ),
        "has_brand": bool(
            source.get("hasBrand")
        ),
        "brand_name": source.get(
            "brandName"
        ),
        "model": source.get(
            "productModel"
        ),
        "usage": source.get("use"),
        "material": source.get(
            "material"
        ),
        "reference_cost_price": source.get(
            "refCostPrice"
        ),
        "inbound_customs": (
            _map_customs_items(
                source.get(
                    "inProductCustomsInfo"
                )
            )
        ),
        "outbound_customs": (
            _map_outbound_customs(
                source.get(
                    "outProductCustomsInfo"
                )
            )
        ),
        "warehouses": (
            _map_warehouse_items(
                source.get("warehouseInfo")
            )
        ),
    })

    return product


# ==================== 查询参数转换 ====================


def map_product_list_query(
    query: dict[str, Any],
) -> dict[str, Any]:
    """将统一查询参数转换为元仓参数。"""

    field_mapping = {
        "page": "page",
        "page_size": "prePage",
        "customer_sku": "customerSku",
        "category_id": "categoryId",
        "created_at_from": "createTimeFrom",
        "created_at_to": "createTimeTo",
    }

    result = {}

    for source_name, target_name in (
        field_mapping.items()
    ):
        value = query.get(source_name)

        # 保留数字0，只过滤未提交值和空字符串
        if value is not None and value != "":
            result[target_name] = value

    return result