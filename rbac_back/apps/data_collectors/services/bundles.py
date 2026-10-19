"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 组合商品数据采集编排服务
"""

from django.db import DatabaseError

from apps.data_collectors.collectors.base import (
    BaseCollector,
)
from apps.data_collectors.collectors.exceptions import (
    CollectorResponseError,
)
from apps.products.services.bundle_sync import (
    BundleSyncService,
)


class BundleCollectionService:
    """编排组合商品采集及数据库同步。"""

    def __init__(
        self,
        collector: BaseCollector,
        sync_service=None,
    ):
        """初始化采集器和同步服务。"""

        self.collector = collector
        self.sync_service = (
            sync_service
            or BundleSyncService()
        )

    # ==================== 执行完整采集 ====================

    def run(self) -> dict:
        """采集组合商品并逐条同步到数据库。"""

        # ==================== 完整数据采集 ====================

        collected_bundles = (
            self.collector.collect()
        )

        if not isinstance(
                collected_bundles,
                list,
        ):
            raise CollectorResponseError(
                "组合商品采集结果必须是列表"
            )

        # ==================== 同步结果初始化 ====================

        result = {
            "total": len(collected_bundles),
            "created": 0,
            "updated": 0,
            "deactivated": 0,
            "failed": 0,
            "errors": [],
        }

        active_external_ids = []

        # ==================== 逐条保存组合商品 ====================

        for collected_bundle in (
                collected_bundles
        ):
            try:
                unused_bundle, created = (
                    self.sync_service.save_bundle(
                        collected_bundle
                    )
                )
            except DatabaseError as error:
                result["failed"] += 1
                result["errors"].append({
                    "bundle_sku": getattr(
                        collected_bundle,
                        "bundle_sku",
                        "",
                    ),
                    "message": str(error),
                })

                continue

            active_external_ids.append(
                collected_bundle.external_id
            )

            if created:
                result["created"] += 1
            else:
                result["updated"] += 1

        # ==================== 缺失组合失效处理 ====================

        # 只有全部组合都保存成功时，才允许处理本次
        # 完整采集中没有出现的历史组合。
        if result["failed"] == 0:
            result["deactivated"] = (
                self.sync_service
                .deactivate_missing_bundles(
                    provider_code=(
                        self.collector.source_name
                    ),
                    active_external_ids=(
                        active_external_ids
                    ),
                )
            )

        return result
