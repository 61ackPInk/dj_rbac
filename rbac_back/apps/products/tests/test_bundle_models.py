"""
-*- coding: utf-8 -*-
@File  : test_bundle_models.py
@Author: 61ackPink
@Time : 2026/10/14 17:50
@Desc : 组合商品模型测试
"""

from django.db import (
    IntegrityError,
    transaction,
)
from django.test import TestCase
from django.utils import timezone

from apps.products.models import (
    ProductBundle,
    ProductBundleItem,
)


class ProductBundleModelTests(TestCase):
    """组合商品及组成明细模型测试"""

    def create_bundle(
        self,
        *,
        provider_code="yuancang",
        external_id="496030",
        bundle_sku="SET-002-SUPER-1",
    ):
        """创建测试使用的组合商品。"""

        return ProductBundle.objects.create(
            provider_code=provider_code,
            external_id=external_id,
            bundle_sku=bundle_sku,
            name="铃兰杯礼盒",
            source_status="1",
            source_status_name="启用",
            collected_at=timezone.now(),
            is_active=True,
        )

    def test_create_bundle_and_items(self):
        """可以创建组合商品及其组成明细。"""

        bundle = self.create_bundle()

        first_item = ProductBundleItem.objects.create(
            bundle=bundle,
            provider_sku=(
                "YC7832-SET-002-SUPER"
            ),
            customer_sku="SET-002-SUPER",
            name="铃兰杯礼盒",
            required_quantity=1,
            source_status="1",
            source_status_name="正常",
            sort_order=0,
        )

        second_item = ProductBundleItem.objects.create(
            bundle=bundle,
            provider_sku=(
                "YC7832-white-bag-s"
            ),
            customer_sku="white-bag-s",
            name="白色礼品袋",
            required_quantity=2,
            source_status="1",
            source_status_name="正常",
            sort_order=1,
        )

        self.assertEqual(
            bundle.items.count(),
            2,
        )

        self.assertEqual(
            first_item.required_quantity,
            1,
        )

        self.assertEqual(
            second_item.required_quantity,
            2,
        )

        self.assertEqual(
            str(bundle),
            "SET-002-SUPER-1（铃兰杯礼盒）",
        )

        self.assertEqual(
            str(second_item),
            (
                "SET-002-SUPER-1"
                " → white-bag-s × 2"
            ),
        )

    def test_external_id_is_unique_in_provider(self):
        """同一来源中的外部记录ID不能重复。"""

        self.create_bundle()

        with self.assertRaises(
            IntegrityError,
        ):
            with transaction.atomic():
                self.create_bundle(
                    external_id="496030",
                    bundle_sku="OTHER-BUNDLE",
                )

    def test_bundle_sku_is_unique_in_provider(self):
        """同一来源中的组合SKU不能重复。"""

        self.create_bundle()

        with self.assertRaises(
            IntegrityError,
        ):
            with transaction.atomic():
                self.create_bundle(
                    external_id="496031",
                    bundle_sku="SET-002-SUPER-1",
                )

    def test_same_bundle_sku_can_exist_in_other_provider(
        self,
    ):
        """不同数据来源可以存在相同组合SKU。"""

        self.create_bundle()

        other_bundle = self.create_bundle(
            provider_code="other_erp",
            external_id="496030",
            bundle_sku="SET-002-SUPER-1",
        )

        self.assertEqual(
            ProductBundle.objects.count(),
            2,
        )

        self.assertEqual(
            other_bundle.provider_code,
            "other_erp",
        )

    def test_customer_sku_is_unique_in_bundle(self):
        """同一组合中不能保存重复子SKU。"""

        bundle = self.create_bundle()

        ProductBundleItem.objects.create(
            bundle=bundle,
            customer_sku="ARO-001",
            required_quantity=1,
        )

        with self.assertRaises(
            IntegrityError,
        ):
            with transaction.atomic():
                ProductBundleItem.objects.create(
                    bundle=bundle,
                    customer_sku="ARO-001",
                    required_quantity=2,
                )

    def test_same_customer_sku_can_exist_in_other_bundle(
        self,
    ):
        """不同组合可以使用相同子SKU。"""

        first_bundle = self.create_bundle()

        second_bundle = self.create_bundle(
            external_id="496031",
            bundle_sku="SET-001-SUPER-1",
        )

        ProductBundleItem.objects.create(
            bundle=first_bundle,
            customer_sku="white-bag-s",
            required_quantity=1,
        )

        ProductBundleItem.objects.create(
            bundle=second_bundle,
            customer_sku="white-bag-s",
            required_quantity=1,
        )

        self.assertEqual(
            ProductBundleItem.objects.count(),
            2,
        )

    def test_required_quantity_must_be_greater_than_zero(
        self,
    ):
        """组成数量不能为零。"""

        bundle = self.create_bundle()

        with self.assertRaises(
            IntegrityError,
        ):
            with transaction.atomic():
                ProductBundleItem.objects.create(
                    bundle=bundle,
                    customer_sku="ARO-001",
                    required_quantity=0,
                )

    def test_delete_bundle_cascades_items(self):
        """删除组合时同时删除组成明细。"""

        bundle = self.create_bundle()

        ProductBundleItem.objects.create(
            bundle=bundle,
            customer_sku="ARO-001",
            required_quantity=1,
        )

        bundle.delete()

        self.assertEqual(
            ProductBundleItem.objects.count(),
            0,
        )