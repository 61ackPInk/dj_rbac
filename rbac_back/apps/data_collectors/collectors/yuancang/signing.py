"""
-*- coding: utf-8 -*-
@File  : signing.py
@Author: 61ackPink
@Time : 2026/10/15 16:45
@Desc : 元仓网页请求动态签名生成
"""

import time
from typing import Any

from apps.data_collectors.collectors.yuancang.crypto import (
    encrypt_with_public_key,
)


# ==================== 签名原文生成 ====================


def build_signature_source(
        payload: dict[str, Any],
        timestamp_ms: int,
) -> str:
    """
    生成元仓请求签名原文。

    与元仓网页逻辑保持一致：
    请求字段名按原始顺序排列，
    最后追加当前毫秒时间。
    """

    if not isinstance(payload, dict):
        raise ValueError(
            "签名请求参数必须是字典"
        )

    if not isinstance(timestamp_ms, int):
        raise ValueError(
            "签名时间戳必须是整数"
        )

    field_names = [
        field_name
        for field_name, value in payload.items()
        if value is not None
    ]

    signature_parts = [
        *field_names,
        f"_t&{timestamp_ms}",
    ]

    return "|".join(signature_parts)


# ==================== 动态签名生成 ====================


def generate_request_sign(
        payload: dict[str, Any],
        public_key: str,
        timestamp_ms: int | None = None,
) -> str:
    """生成元仓请求头使用的 RSA sign。"""

    if timestamp_ms is None:
        timestamp_ms = (
            time.time_ns() // 1_000_000
        )

    signature_source = (
        build_signature_source(
            payload,
            timestamp_ms,
        )
    )

    return encrypt_with_public_key(
        signature_source,
        public_key,
    )