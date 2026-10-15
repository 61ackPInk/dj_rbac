"""
-*- coding: utf-8 -*-
@File  : bundle_sync.py
@Author: 61ackPink
@Time : 2026/10/15 14:47
@Desc : 组合商品采集数据同步服务
"""

from django.db import transaction
from django.utils import timezone

from apps.data_collectors.schemas.bundles import (
    CollectedBundle,
)
from apps.products.models import (
    ProductBundle,
    ProductBundleItem,
)


class BundleSyncService:
    """将标准采集数据同步到商品系统。"""

    # ==================== 单个组合商品同步 ====================

    @transaction.atomic
    def save_bundle(
        self,
        collected_bundle: CollectedBundle,
    ) -> tuple[ProductBundle, bool]:
        """新增或更新一个组合商品及其组成明细。"""

        collected_at = timezone.now()

        bundle, created = (
            ProductBundle.objects.update_or_create(
                provider_code=(
                    collected_bundle.provider_code
                ),
                external_id=(
                    collected_bundle.external_id
                ),
                defaults={
                    "bundle_sku": (
                        collected_bundle.bundle_sku
                    ),
                    "name": collected_bundle.name,
                    "image_url": (
                        collected_bundle.image_url
                    ),
                    "source_status": (
                        collected_bundle.source_status
                    ),
                    "source_status_name": (
                        collected_bundle
                        .source_status_name
                    ),
                    "source_created_at": (
                        collected_bundle
                        .source_created_at
                    ),
                    "source_updated_at": (
                        collected_bundle
                        .source_updated_at
                    ),
                    "collected_at": collected_at,
                    "is_active": True,
                },
            )
        )

        # 每次使用本次采集到的完整组成关系，
        # 替换数据库中的旧组成明细。
        bundle.items.all().delete()

        ProductBundleItem.objects.bulk_create([
            ProductBundleItem(
                bundle=bundle,
                provider_sku=(
                    collected_item.provider_sku
                ),
                customer_sku=(
                    collected_item.customer_sku
                ),
                name=collected_item.name,
                image_url=(
                    collected_item.image_url
                ),
                required_quantity=(
                    collected_item.required_quantity
                ),
                source_status=(
                    collected_item.source_status
                ),
                source_status_name=(
                    collected_item
                    .source_status_name
                ),
                sort_order=(
                    collected_item.sort_order
                ),
            )
            for collected_item
            in collected_bundle.items
        ])

        return bundle, created