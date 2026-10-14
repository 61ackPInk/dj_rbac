"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 组合商品采集结果标准结构
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ==================== 组合商品子项结构 ====================


@dataclass
class CollectedBundleItem:
    """采集并标准化后的组合商品子项。"""

    provider_sku: str
    customer_sku: str
    name: str = ""
    image_url: str = ""
    required_quantity: int = 1
    source_status: str = ""
    source_status_name: str = ""
    sort_order: int = 0


# ==================== 组合商品结构 ====================


@dataclass
class CollectedBundle:
    """采集并标准化后的组合商品。"""

    provider_code: str
    external_id: str
    bundle_sku: str
    name: str = ""
    image_url: str = ""
    source_status: str = ""
    source_status_name: str = ""
    source_created_at: Optional[datetime] = None
    source_updated_at: Optional[datetime] = None
    items: list[CollectedBundleItem] = field(
        default_factory=list,
    )