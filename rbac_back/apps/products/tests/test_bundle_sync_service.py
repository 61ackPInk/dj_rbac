"""
-*- coding: utf-8 -*-
@File  : test_bundle_sync_service.py
@Author: 61ackPink
@Time : 2026/10/15 14:47
@Desc : 组合商品采集数据同步服务测试
"""

from django.test import TestCase

from apps.data_collectors.schemas.bundles import (
    CollectedBundle,
    CollectedBundleItem,
)
from apps.products.models import (
    ProductBundle,
    ProductBundleItem,
)
from apps.products.services.bundle_sync import (
    BundleSyncService,
)


class BundleSyncServiceTests(TestCase):
    """组合商品同步服务测试。"""

    def setUp(self):
        """初始化同步服务。"""

        self.service = BundleSyncService()

    def create_collected_bundle(self):
        """创建标准组合商品测试数据。"""

        return CollectedBundle(
            provider_code="yuancang",
            external_id="496030",
            bundle_sku="SET-002-SUPER-1",
            name="铃兰杯礼盒",
            source_status="1",
            source_status_name="启用",
            items=[
                CollectedBundleItem(
                    provider_sku=(
                        "YC7832-SET-002-SUPER"
                    ),
                    customer_sku="SET-002-SUPER",
                    name="铃兰杯礼盒",
                    required_quantity=1,
                    sort_order=0,
                ),
                CollectedBundleItem(
                    provider_sku=(
                        "YC7832-white-bag-s"
                    ),
                    customer_sku="white-bag-s",
                    name="白色礼品袋",
                    required_quantity=1,
                    sort_order=1,
                ),
            ],
        )

    def test_create_bundle_and_items(self):
        """首次同步会创建组合及组成明细。"""

        bundle, created = (
            self.service.save_bundle(
                self.create_collected_bundle()
            )
        )

        self.assertTrue(created)
        self.assertEqual(
            ProductBundle.objects.count(),
            1,
        )
        self.assertEqual(
            ProductBundleItem.objects.count(),
            2,
        )
        self.assertEqual(
            bundle.items.get(
                customer_sku="white-bag-s"
            ).required_quantity,
            1,
        )
        self.assertTrue(bundle.is_active)

    def test_existing_bundle_is_updated(self):
        """重复同步会更新原记录而不重复创建。"""

        collected_bundle = (
            self.create_collected_bundle()
        )

        first_bundle, first_created = (
            self.service.save_bundle(
                collected_bundle
            )
        )

        collected_bundle.name = "更新后的组合名称"
        collected_bundle.items = [
            CollectedBundleItem(
                provider_sku=(
                    "YC7832-white-bag-s"
                ),
                customer_sku="white-bag-s",
                name="白色礼品袋",
                required_quantity=2,
                sort_order=0,
            ),
        ]

        second_bundle, second_created = (
            self.service.save_bundle(
                collected_bundle
            )
        )

        self.assertTrue(first_created)
        self.assertFalse(second_created)
        self.assertEqual(
            first_bundle.id,
            second_bundle.id,
        )
        self.assertEqual(
            ProductBundle.objects.count(),
            1,
        )
        self.assertEqual(
            ProductBundleItem.objects.count(),
            1,
        )

        second_bundle.refresh_from_db()

        self.assertEqual(
            second_bundle.name,
            "更新后的组合名称",
        )
        self.assertEqual(
            second_bundle.items.get().required_quantity,
            2,
        )

    def test_inactive_bundle_becomes_active(self):
        """再次采集到的组合会恢复为有效状态。"""

        bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle()
            )
        )

        bundle.is_active = False
        bundle.save(
            update_fields=[
                "is_active",
                "update_time",
            ]
        )

        updated_bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle()
            )
        )

        self.assertTrue(
            updated_bundle.is_active
        )