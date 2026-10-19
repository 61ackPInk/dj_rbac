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

    # ==================== 缺失组合失效处理 ====================

    @transaction.atomic
    def deactivate_missing_bundles(
        self,
        *,
        provider_code: str,
        active_external_ids: list[str],
    ) -> int:
        """
        将完整采集中未出现的来源组合标记为无效。

        只处理指定数据来源下当前仍然有效的组合，不删除数据库记录。
        如果后续重新采集到该组合，save_bundle 会重新将其恢复为有效状态。
        """

        # ==================== 参数校验 ====================

        normalized_provider_code = provider_code.strip()

        if not normalized_provider_code:
            raise ValueError("数据来源编码不能为空")

        normalized_external_ids = {
            str(external_id).strip()
            for external_id in active_external_ids
            if external_id is not None
            and str(external_id).strip()
        }

        # 防止第三方接口异常返回空列表时误伤全部组合数据
        if not normalized_external_ids:
            raise ValueError(
                "完整采集结果为空，拒绝批量失效组合商品"
            )

        # ==================== 查询缺失组合 ====================

        missing_queryset = ProductBundle.objects.filter(
            provider_code=normalized_provider_code,
            is_active=True,
        ).exclude(
            external_id__in=normalized_external_ids,
        )

        # ==================== 批量标记无效 ====================

        return missing_queryset.update(
            is_active=False,
            update_time=timezone.now(),
        )