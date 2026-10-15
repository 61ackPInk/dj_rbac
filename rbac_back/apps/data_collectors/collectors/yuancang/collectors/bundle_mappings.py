"""
-*- coding: utf-8 -*-
@File  : bundle_mappings.py
@Author: 61ackPink
@Time : 2026/10/15 17:59
@Desc : 元仓组合映射数据采集器
"""

from datetime import date, timedelta


# ==================== 组合映射采集常量 ====================

# 元仓要求创建时间范围不能超过3个月。
# 这里使用包含首尾在内的90天窗口，
# 避免不同自然月份天数造成接口拒绝。
MAX_DATE_RANGE_DAYS = 89


# ==================== 日期区间拆分 ====================


def build_date_ranges(
        start_date: date,
        end_date: date,
) -> list[tuple[date, date]]:
    """将采集日期拆分为连续的安全区间。"""

    if not isinstance(start_date, date):
        raise ValueError(
            "采集开始日期必须是date类型"
        )

    if not isinstance(end_date, date):
        raise ValueError(
            "采集结束日期必须是date类型"
        )

    if start_date > end_date:
        raise ValueError(
            "采集开始日期不能晚于结束日期"
        )

    date_ranges = []
    current_start = start_date

    while current_start <= end_date:
        current_end = min(
            current_start + timedelta(
                days=MAX_DATE_RANGE_DAYS
            ),
            end_date,
        )

        date_ranges.append(
            (
                current_start,
                current_end,
            )
        )

        current_start = (
            current_end + timedelta(days=1)
        )

    return date_ranges


# ==================== 分页请求体构造 ====================


def build_bundle_mapping_payload(
        *,
        start_date: date,
        end_date: date,
        page: int,
        page_size: int,
) -> dict:
    """构造元仓组合映射列表请求体。"""

    if start_date > end_date:
        raise ValueError(
            "请求开始日期不能晚于结束日期"
        )

    if page < 1:
        raise ValueError(
            "请求页码必须大于或等于1"
        )

    if page_size < 1:
        raise ValueError(
            "每页数量必须大于或等于1"
        )

    # 字段顺序与元仓网页请求保持一致，
    # 该顺序同时用于生成动态sign。
    return {
        "createdAt": [
            (
                f"{start_date.isoformat()}"
                " 00:00:00"
            ),
            (
                f"{end_date.isoformat()}"
                " 23:59:59"
            ),
        ],
        "matchType": "exact",
        "searchType": "originSkuName",
        "page": page,
        "prePage": page_size,
    }