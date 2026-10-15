"""
-*- coding: utf-8 -*-
@File  : test_yuancang_bundle_collector.py
@Author: 61ackPink
@Time : 2026/10/15 17:59
@Desc : 元仓组合映射采集器测试
"""

from datetime import date, timedelta

from django.test import SimpleTestCase

from apps.data_collectors.collectors.yuancang.collectors.bundle_mappings import (
    MAX_DATE_RANGE_DAYS,
    build_bundle_mapping_payload,
    build_date_ranges,
)


class YuancangBundleCollectorTests(
    SimpleTestCase
):
    """元仓组合映射采集器测试。"""

    def test_short_period_has_one_range(self):
        """不足90天时只生成一个区间。"""

        result = build_date_ranges(
            date(2026, 9, 10),
            date(2026, 10, 15),
        )

        self.assertEqual(
            result,
            [
                (
                    date(2026, 9, 10),
                    date(2026, 10, 15),
                )
            ],
        )

    def test_long_period_is_split_continuously(
        self,
    ):
        """长时间范围会拆分为连续区间。"""

        result = build_date_ranges(
            date(2026, 1, 1),
            date(2026, 10, 15),
        )

        self.assertEqual(
            result[0][0],
            date(2026, 1, 1),
        )
        self.assertEqual(
            result[-1][1],
            date(2026, 10, 15),
        )

        for index, date_range in enumerate(
                result
        ):
            range_start, range_end = date_range

            self.assertLessEqual(
                (
                    range_end - range_start
                ).days,
                MAX_DATE_RANGE_DAYS,
            )

            if index > 0:
                previous_end = (
                    result[index - 1][1]
                )

                self.assertEqual(
                    range_start,
                    previous_end
                    + timedelta(days=1),
                )

    def test_invalid_date_range_raises_error(
        self,
    ):
        """开始日期晚于结束日期时拒绝拆分。"""

        with self.assertRaisesRegex(
            ValueError,
            "开始日期不能晚于结束日期",
        ):
            build_date_ranges(
                date(2026, 10, 15),
                date(2026, 9, 10),
            )

    def test_build_bundle_mapping_payload(self):
        """生成字段顺序固定的分页请求体。"""

        result = build_bundle_mapping_payload(
            start_date=date(2026, 9, 10),
            end_date=date(2026, 10, 15),
            page=2,
            page_size=20,
        )

        self.assertEqual(
            list(result.keys()),
            [
                "createdAt",
                "matchType",
                "searchType",
                "page",
                "prePage",
            ],
        )

        self.assertEqual(
            result,
            {
                "createdAt": [
                    "2026-09-10 00:00:00",
                    "2026-10-15 23:59:59",
                ],
                "matchType": "exact",
                "searchType": "originSkuName",
                "page": 2,
                "prePage": 20,
            },
        )

    def test_invalid_page_raises_error(self):
        """页码小于1时拒绝构造请求。"""

        with self.assertRaisesRegex(
            ValueError,
            "请求页码必须大于或等于1",
        ):
            build_bundle_mapping_payload(
                start_date=date(
                    2026,
                    9,
                    10,
                ),
                end_date=date(
                    2026,
                    10,
                    15,
                ),
                page=0,
                page_size=20,
            )