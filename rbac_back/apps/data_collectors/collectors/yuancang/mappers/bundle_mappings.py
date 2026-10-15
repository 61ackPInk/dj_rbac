"""
-*- coding: utf-8 -*-
@File  : bundle_mappings.py
@Author: 61ackPink
@Time : 2026/10/15 14:39
@Desc : 元仓组合映射采集数据转换
"""

from datetime import datetime
from typing import Any

from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.data_collectors.schemas.bundles import (
    CollectedBundle,
    CollectedBundleItem,
)


# ==================== 基础字段转换 ====================


def _to_string(value: Any) -> str:
    """将来源字段安全转换为字符串。"""

    if value is None:
        return ""

    return str(value).strip()


def _parse_source_datetime(
        value: Any,
) -> datetime | None:
    """解析元仓返回的日期时间。"""

    if value is None or value == "":
        return None

    if isinstance(value, datetime):
        parsed_value = value
    elif isinstance(value, str):
        parsed_value = parse_datetime(value)
    else:
        parsed_value = None

    if parsed_value is None:
        raise CollectorResponseError(
            f"无法解析元仓日期时间：{value}"
        )

    if timezone.is_naive(parsed_value):
        parsed_value = timezone.make_aware(
            parsed_value,
            timezone.get_current_timezone(),
        )

    return parsed_value


def _parse_quantity(value: Any) -> int:
    """解析组合商品子项数量。"""

    if value is None or value == "":
        return 1

    try:
        quantity = int(value)
    except (TypeError, ValueError) as error:
        raise CollectorResponseError(
            f"组合商品子项数量无效：{value}"
        ) from error

    if quantity < 1:
        raise CollectorResponseError(
            f"组合商品子项数量必须大于零：{value}"
        )

    return quantity


# ==================== 组合商品子项转换 ====================


def _map_bundle_items(
        source: Any,
) -> list[CollectedBundleItem]:
    """转换并合并组合商品子项。"""

    if source is None:
        source = []

    if not isinstance(source, list):
        raise CollectorResponseError(
            "元仓组合商品的 mapItemList 必须是列表"
        )

    merged_items = {}

    for source_item in source:
        if not isinstance(source_item, dict):
            raise CollectorResponseError(
                "元仓组合商品子项必须是对象"
            )

        customer_sku = _to_string(
            source_item.get("customerSku")
        )

        if not customer_sku:
            raise CollectorResponseError(
                "元仓组合商品子项缺少 customerSku"
            )

        quantity = _parse_quantity(
            source_item.get("quantity")
        )

        # 相同 customer_sku 合并并累加所需数量
        if customer_sku in merged_items:
            merged_items[
                customer_sku
            ].required_quantity += quantity

            continue

        merged_items[customer_sku] = (
            CollectedBundleItem(
                provider_sku=_to_string(
                    source_item.get("productSku")
                ),
                customer_sku=customer_sku,
                name=_to_string(
                    source_item.get("productName")
                ),
                image_url=_to_string(
                    source_item.get("imageUrl")
                ),
                required_quantity=quantity,
                source_status=_to_string(
                    source_item.get(
                        "productStatus"
                    )
                ),
                source_status_name=_to_string(
                    source_item.get(
                        "productStatusDescription"
                    )
                ),
                sort_order=len(merged_items),
            )
        )

    return list(merged_items.values())


# ==================== 单个组合商品转换 ====================


def map_bundle_record(
        source: Any,
) -> CollectedBundle:
    """将元仓组合映射转换为标准结构。"""

    if not isinstance(source, dict):
        raise CollectorResponseError(
            "元仓组合商品记录必须是对象"
        )

    external_id = _to_string(
        source.get("id")
    )
    bundle_sku = _to_string(
        source.get("originSku")
    )

    if not external_id:
        raise CollectorResponseError(
            "元仓组合商品缺少 id"
        )

    if not bundle_sku:
        raise CollectorResponseError(
            "元仓组合商品缺少 originSku"
        )

    return CollectedBundle(
        provider_code="yuancang",
        external_id=external_id,
        bundle_sku=bundle_sku,
        name=_to_string(
            source.get("originSkuName")
        ),
        image_url=_to_string(
            source.get("imageUrls")
        ),
        source_status=_to_string(
            source.get("status")
        ),
        source_status_name=_to_string(
            source.get("statusDescription")
        ),
        source_created_at=(
            _parse_source_datetime(
                source.get("createdAt")
            )
        ),
        source_updated_at=(
            _parse_source_datetime(
                source.get("updatedAt")
            )
        ),
        items=_map_bundle_items(
            source.get("mapItemList")
        ),
    )


# ==================== 组合商品列表转换 ====================


def map_bundle_list_response(
        source: Any,
) -> list[CollectedBundle]:
    """转换元仓组合商品列表响应。"""

    if not isinstance(source, dict):
        raise CollectorResponseError(
            "元仓组合商品响应必须是对象"
        )

    data = source.get("data")

    if not isinstance(data, dict):
        raise CollectorResponseError(
            "元仓组合商品响应缺少 data"
        )

    source_list = data.get("list")

    if not isinstance(source_list, list):
        raise CollectorResponseError(
            "元仓组合商品响应中的 list 必须是列表"
        )

    return [
        map_bundle_record(item)
        for item in source_list
    ]