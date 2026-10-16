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

    # ==================== 测试数据构造 ====================

    def create_collected_bundle(
            self,
            *,
            provider_code: str = "yuancang",
            external_id: str = "496030",
            bundle_sku: str = "SET-002-SUPER-1",
    ) -> CollectedBundle:
        """创建标准组合商品测试数据。"""

        return CollectedBundle(
            provider_code=provider_code,
            external_id=external_id,
            bundle_sku=bundle_sku,
            name=f"测试组合-{bundle_sku}",
            source_status="1",
            source_status_name="启用",
            items=[
                CollectedBundleItem(
                    provider_sku=(
                        f"PROVIDER-{bundle_sku}"
                    ),
                    customer_sku=(
                        f"CHILD-{bundle_sku}"
                    ),
                    name=f"测试子商品-{bundle_sku}",
                    required_quantity=1,
                    sort_order=0,
                ),
                CollectedBundleItem(
                    provider_sku=(
                        f"PROVIDER-GIFT-{bundle_sku}"
                    ),
                    customer_sku=(
                        f"GIFT-{bundle_sku}"
                    ),
                    name=f"测试赠品-{bundle_sku}",
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
                customer_sku=(
                    "CHILD-SET-002-SUPER-1"
                )
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

    # ==================== 缺失组合失效测试 ====================

    def test_deactivate_missing_bundles(self):
        """完整同步后应将未出现的同来源组合标记为无效。"""

        first_bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle(
                    external_id="496030",
                    bundle_sku="SET-002-SUPER-1",
                )
            )
        )

        second_bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle(
                    external_id="496031",
                    bundle_sku="SET-001-SUPER-1",
                )
            )
        )

        other_provider_bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle(
                    provider_code="other_erp",
                    external_id="496031",
                    bundle_sku="OTHER-SET-001",
                )
            )
        )

        updated_count = (
            self.service.deactivate_missing_bundles(
                provider_code="yuancang",
                active_external_ids=["496030"],
            )
        )

        first_bundle.refresh_from_db()
        second_bundle.refresh_from_db()
        other_provider_bundle.refresh_from_db()

        self.assertEqual(updated_count, 1)
        self.assertTrue(first_bundle.is_active)
        self.assertFalse(second_bundle.is_active)
        self.assertTrue(
            other_provider_bundle.is_active
        )

    def test_deactivate_missing_bundles_rejects_empty_result(
            self,
    ):
        """完整采集结果为空时不应批量失效现有组合。"""

        bundle, unused_created = (
            self.service.save_bundle(
                self.create_collected_bundle()
            )
        )

        with self.assertRaisesMessage(
                ValueError,
                "完整采集结果为空，拒绝批量失效组合商品",
        ):
            self.service.deactivate_missing_bundles(
                provider_code="yuancang",
                active_external_ids=[],
            )

        bundle.refresh_from_db()

        self.assertTrue(bundle.is_active)

    def test_deactivate_missing_bundles_requires_provider_code(self):
        """执行缺失处理时必须提供数据来源编码。"""

        with self.assertRaisesMessage(
            ValueError,
            "数据来源编码不能为空",
        ):
            self.service.deactivate_missing_bundles(
                provider_code=" ",
                active_external_ids=["496030"],
            )