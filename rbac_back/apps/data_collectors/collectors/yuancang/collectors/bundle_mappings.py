"""
-*- coding: utf-8 -*-
@File  : bundle_mappings.py
@Author: 61ackPink
@Time : 2026/10/15 17:59
@Desc : 元仓组合映射数据采集器
"""

from datetime import date, timedelta

from django.utils import timezone

from apps.data_collectors.collectors.base import (
    BaseCollector,
)
from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.data_collectors.collectors.yuancang.client import (
    YuancangWebClient,
)
from apps.data_collectors.collectors.yuancang.configs.bundle_mappings import (
    YuancangBundleMappingConfig,
)
from apps.data_collectors.collectors.yuancang.mappers.bundle_mappings import (
    map_bundle_list_response,
)
from apps.data_collectors.schemas.bundles import (
    CollectedBundle,
)


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

# ==================== 组合映射采集器 ====================


class YuancangBundleMappingCollector(
    BaseCollector
):
    """采集元仓全部组合映射数据。"""

    def __init__(
        self,
        *,
        client: YuancangWebClient,
        config: YuancangBundleMappingConfig,
        end_date: date | None = None,
    ):
        """初始化客户端和采集配置。"""

        self.client = client
        self.config = config
        self.end_date = end_date

    # ==================== 数据来源 ====================

    @property
    def source_name(self):
        """返回采集数据来源名称。"""

        return "yuancang"

    # ==================== 完整数据采集 ====================

    def collect(
        self,
    ) -> list[CollectedBundle]:
        """按日期区间和分页采集全部组合映射。"""

        collection_end_date = (
            self.end_date
            or timezone.localdate()
        )

        date_ranges = build_date_ranges(
            self.config.start_date,
            collection_end_date,
        )

        collected_by_external_id = {}

        for range_start, range_end in (
                date_ranges
        ):
            range_bundles = (
                self._collect_date_range(
                    range_start=range_start,
                    range_end=range_end,
                )
            )

            for bundle in range_bundles:
                # 不同日期区间如果返回相同记录，
                # 使用external_id覆盖并完成去重。
                collected_by_external_id[
                    bundle.external_id
                ] = bundle

        return list(
            collected_by_external_id.values()
        )

    # ==================== 单个日期区间采集 ====================

    def _collect_date_range(
        self,
        *,
        range_start: date,
        range_end: date,
    ) -> list[CollectedBundle]:
        """采集一个日期区间内的全部分页。"""

        collected_bundles = []
        page = 1

        while True:
            payload = (
                build_bundle_mapping_payload(
                    start_date=range_start,
                    end_date=range_end,
                    page=page,
                    page_size=(
                        self.config.page_size
                    ),
                )
            )

            response = (
                self.client.post_authenticated(
                    url=(
                        self.config
                        .build_list_url(
                            self.client.config
                        )
                    ),
                    payload=payload,
                )
            )

            page_bundles = (
                map_bundle_list_response(
                    response
                )
            )

            total = self._read_total(response)

            collected_bundles.extend(
                page_bundles
            )

            # 空列表表示已经没有下一页。
            if not page_bundles:
                break

            # 当前页已经覆盖total时停止翻页。
            if (
                page * self.config.page_size
                >= total
            ):
                break

            page += 1

        return collected_bundles

    # ==================== 分页总数解析 ====================

    @staticmethod
    def _read_total(
        response: dict,
    ) -> int:
        """读取并校验响应中的总记录数。"""

        data = response.get("data")

        if not isinstance(data, dict):
            raise CollectorResponseError(
                "元仓组合映射响应缺少data"
            )

        raw_total = data.get("total")

        try:
            total = int(raw_total)
        except (TypeError, ValueError) as error:
            raise CollectorResponseError(
                "元仓组合映射响应total无效"
            ) from error

        if total < 0:
            raise CollectorResponseError(
                "元仓组合映射响应total不能小于0"
            )

        return total