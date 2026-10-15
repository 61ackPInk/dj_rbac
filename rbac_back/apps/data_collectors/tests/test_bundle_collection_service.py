"""
-*- coding: utf-8 -*-
@File  : test_bundle_collection_service.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 组合商品数据采集编排服务测试
"""

from django.db import DatabaseError
from django.test import SimpleTestCase

from apps.data_collectors.collectors.base import (
    BaseCollector,
)
from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.data_collectors.schemas.bundles import (
    CollectedBundle,
)
from apps.data_collectors.services.bundles import (
    BundleCollectionService,
)


class FakeBundleCollector(BaseCollector):
    """测试使用的组合商品采集器。"""

    def __init__(self, result):
        self.result = result

    @property
    def source_name(self):
        """返回测试数据来源。"""

        return "fake"

    def collect(self):
        """返回预设采集结果。"""

        return self.result


class FakeBundleSyncService:
    """测试使用的组合商品同步服务。"""

    def __init__(
        self,
        *,
        fail_skus=None,
        existing_skus=None,
    ):
        self.fail_skus = set(
            fail_skus or []
        )
        self.existing_skus = set(
            existing_skus or []
        )

    def save_bundle(
        self,
        collected_bundle,
    ):
        """模拟数据库同步结果。"""

        if (
            collected_bundle.bundle_sku
            in self.fail_skus
        ):
            raise DatabaseError(
                "模拟数据库保存失败"
            )

        created = (
            collected_bundle.bundle_sku
            not in self.existing_skus
        )

        return object(), created


class BundleCollectionServiceTests(
    SimpleTestCase
):
    """组合商品采集编排服务测试。"""

    def create_bundle(
        self,
        external_id,
        bundle_sku,
    ):
        """创建标准组合商品测试数据。"""

        return CollectedBundle(
            provider_code="yuancang",
            external_id=external_id,
            bundle_sku=bundle_sku,
        )

    def test_run_returns_sync_statistics(self):
        """返回新增和更新数量统计。"""

        collector = FakeBundleCollector([
            self.create_bundle(
                "1",
                "BUNDLE-001",
            ),
            self.create_bundle(
                "2",
                "BUNDLE-002",
            ),
        ])

        sync_service = FakeBundleSyncService(
            existing_skus={
                "BUNDLE-002",
            }
        )

        service = BundleCollectionService(
            collector=collector,
            sync_service=sync_service,
        )

        result = service.run()

        self.assertEqual(
            result["total"],
            2,
        )
        self.assertEqual(
            result["created"],
            1,
        )
        self.assertEqual(
            result["updated"],
            1,
        )
        self.assertEqual(
            result["failed"],
            0,
        )
        self.assertEqual(
            result["errors"],
            [],
        )

    def test_database_error_is_recorded(self):
        """单条保存失败会记录并继续处理。"""

        collector = FakeBundleCollector([
            self.create_bundle(
                "1",
                "BUNDLE-001",
            ),
            self.create_bundle(
                "2",
                "BUNDLE-002",
            ),
        ])

        sync_service = FakeBundleSyncService(
            fail_skus={
                "BUNDLE-001",
            }
        )

        service = BundleCollectionService(
            collector=collector,
            sync_service=sync_service,
        )

        result = service.run()

        self.assertEqual(
            result["total"],
            2,
        )
        self.assertEqual(
            result["created"],
            1,
        )
        self.assertEqual(
            result["failed"],
            1,
        )
        self.assertEqual(
            result["errors"][0][
                "bundle_sku"
            ],
            "BUNDLE-001",
        )

    def test_invalid_collection_result_raises_error(
        self,
    ):
        """采集器返回非列表数据时拒绝同步。"""

        collector = FakeBundleCollector(
            {
                "bundle_sku": "BUNDLE-001"
            }
        )

        service = BundleCollectionService(
            collector=collector,
            sync_service=(
                FakeBundleSyncService()
            ),
        )

        with self.assertRaises(
            CollectorResponseError
        ):
            service.run()