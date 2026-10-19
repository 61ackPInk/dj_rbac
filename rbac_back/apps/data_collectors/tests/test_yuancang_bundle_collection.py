"""
-*- coding: utf-8 -*-
@File  : test_yuancang_bundle_collection.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 元仓组合映射完整采集流程测试
"""

from datetime import date
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.data_collectors.collectors.yuancang.collectors.bundle_mappings import (
    YuancangBundleMappingCollector,
)
from apps.data_collectors.collectors.yuancang.configs.bundle_mappings import (
    YuancangBundleMappingConfig,
)
from apps.data_collectors.collectors.yuancang.configs.common import (
    YuancangCommonConfig,
)


class YuancangBundleCollectionTests(
    SimpleTestCase
):
    """元仓组合映射完整采集测试。"""

    def setUp(self):
        """初始化采集器测试配置。"""

        self.common_config = (
            YuancangCommonConfig(
                base_url=(
                    "https://example.com"
                ),
                username="test-user",
                password="test-password",
                timeout_seconds=15,
            )
        )

        self.bundle_config = (
            YuancangBundleMappingConfig(
                start_date=date(
                    2026,
                    9,
                    10,
                ),
                page_size=2,
            )
        )

        self.client = Mock()
        self.client.config = (
            self.common_config
        )

    def create_source_record(
        self,
        external_id,
        bundle_sku,
    ):
        """创建元仓组合映射原始记录。"""

        return {
            "id": external_id,
            "originSku": bundle_sku,
            "originSkuName": bundle_sku,
            "status": 1,
            "statusDescription": "启用",
            "mapItemList": [],
        }

    def create_response(
        self,
        records,
        *,
        total,
        page,
    ):
        """创建元仓分页响应。"""

        return {
            "state": "000001",
            "msg": "请求成功",
            "data": {
                "list": records,
                "total": total,
                "page": page,
                "prePage": 2,
            },
        }

    def test_collects_all_pages(self):
        """采集器会自动请求全部分页。"""

        self.client.post_authenticated.side_effect = [
            self.create_response(
                [
                    self.create_source_record(
                        1,
                        "BUNDLE-001",
                    ),
                    self.create_source_record(
                        2,
                        "BUNDLE-002",
                    ),
                ],
                total=3,
                page=1,
            ),
            self.create_response(
                [
                    self.create_source_record(
                        3,
                        "BUNDLE-003",
                    ),
                ],
                total=3,
                page=2,
            ),
        ]

        collector = (
            YuancangBundleMappingCollector(
                client=self.client,
                config=self.bundle_config,
                end_date=date(
                    2026,
                    10,
                    15,
                ),
            )
        )

        result = collector.collect()

        self.assertEqual(
            collector.source_name,
            "yuancang",
        )
        self.assertEqual(
            len(result),
            3,
        )
        self.assertEqual(
            [
                item.bundle_sku
                for item in result
            ],
            [
                "BUNDLE-001",
                "BUNDLE-002",
                "BUNDLE-003",
            ],
        )
        self.assertEqual(
            self.client
            .post_authenticated
            .call_count,
            2,
        )

        second_payload = (
            self.client
            .post_authenticated
            .call_args_list[1]
            .kwargs["payload"]
        )

        self.assertEqual(
            second_payload["page"],
            2,
        )

    def test_duplicate_external_id_is_merged(
        self,
    ):
        """不同日期区间的相同记录会去重。"""

        self.bundle_config = (
            YuancangBundleMappingConfig(
                start_date=date(
                    2026,
                    1,
                    1,
                ),
                page_size=20,
            )
        )

        self.client.post_authenticated.side_effect = [
            self.create_response(
                [
                    self.create_source_record(
                        1,
                        "BUNDLE-001",
                    )
                ],
                total=1,
                page=1,
            ),
            self.create_response(
                [
                    self.create_source_record(
                        1,
                        "BUNDLE-001",
                    )
                ],
                total=1,
                page=1,
            ),
        ]

        collector = (
            YuancangBundleMappingCollector(
                client=self.client,
                config=self.bundle_config,
                end_date=date(
                    2026,
                    4,
                    1,
                ),
            )
        )

        result = collector.collect()

        self.assertEqual(
            len(result),
            1,
        )
        self.assertEqual(
            self.client
            .post_authenticated
            .call_count,
            2,
        )

    def test_empty_result_stops_pagination(
        self,
    ):
        """空结果会结束当前区间分页。"""

        self.client.post_authenticated.return_value = (
            self.create_response(
                [],
                total=0,
                page=1,
            )
        )

        collector = (
            YuancangBundleMappingCollector(
                client=self.client,
                config=self.bundle_config,
                end_date=date(
                    2026,
                    10,
                    15,
                ),
            )
        )

        result = collector.collect()

        self.assertEqual(result, [])
        self.assertEqual(
            self.client
            .post_authenticated
            .call_count,
            1,
        )

    def test_invalid_total_raises_error(self):
        """无效total会抛出响应异常。"""

        self.client.post_authenticated.return_value = {
            "state": "000001",
            "msg": "请求成功",
            "data": {
                "list": [],
                "total": "invalid",
                "page": 1,
                "prePage": 2,
            },
        }

        collector = (
            YuancangBundleMappingCollector(
                client=self.client,
                config=self.bundle_config,
                end_date=date(
                    2026,
                    10,
                    15,
                ),
            )
        )

        with self.assertRaisesRegex(
            CollectorResponseError,
            "total无效",
        ):
            collector.collect()

    @patch(
        (
            "apps.data_collectors.collectors"
            ".yuancang.collectors.bundle_mappings"
            ".timezone.localdate"
        ),
        return_value=date(
            2026,
            10,
            15,
        ),
    )
    def test_collect_uses_local_date_by_default(
        self,
        localdate,
    ):
        """未指定结束日期时使用系统本地日期。"""

        self.client.post_authenticated.return_value = (
            self.create_response(
                [],
                total=0,
                page=1,
            )
        )

        collector = (
            YuancangBundleMappingCollector(
                client=self.client,
                config=self.bundle_config,
            )
        )

        result = collector.collect()

        self.assertEqual(result, [])
        localdate.assert_called_once_with()

        self.assertEqual(
            self.client
            .post_authenticated
            .call_count,
            1,
        )