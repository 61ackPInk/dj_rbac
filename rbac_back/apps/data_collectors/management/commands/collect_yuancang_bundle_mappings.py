"""
-*- coding: utf-8 -*-
@File  : collect_yuancang_bundle_mappings.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 手动采集元仓组合映射管理命令
"""

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.data_collectors.collectors.exceptions import (
    DataCollectorError,
)
from apps.data_collectors.collectors.yuancang.client import (
    YuancangWebClient,
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
from apps.data_collectors.services.bundles import (
    BundleCollectionService,
)


class Command(BaseCommand):
    """采集并保存元仓组合映射。"""

    help = "采集元仓组合映射并同步到本地数据库"

    # ==================== 服务构造 ====================

    def build_service(
        self,
    ) -> BundleCollectionService:
        """根据应用配置构造采集服务。"""

        common_config = (
            YuancangCommonConfig
            .from_environment()
        )

        bundle_config = (
            YuancangBundleMappingConfig
            .from_environment()
        )

        client = YuancangWebClient(
            config=common_config,
        )

        collector = (
            YuancangBundleMappingCollector(
                client=client,
                config=bundle_config,
            )
        )

        return BundleCollectionService(
            collector=collector,
        )

    # ==================== 命令执行 ====================

    def handle(self, *args, **options):
        """执行组合映射采集任务。"""

        self.stdout.write(
            "开始采集元仓组合映射..."
        )

        try:
            result = (
                self.build_service().run()
            )
        except (
            DataCollectorError,
            ValueError,
        ) as error:
            raise CommandError(
                f"组合映射采集失败：{error}"
            ) from error

        self.stdout.write(
            (
                "采集结果："
                f"总数 {result['total']}，"
                f"新增 {result['created']}，"
                f"更新 {result['updated']}，"
                f"失效 {result['deactivated']}，"
                f"失败 {result['failed']}"
            )
        )

        if result["failed"]:
            for error_item in result["errors"]:
                self.stderr.write(
                    (
                        "保存失败："
                        f"{error_item['bundle_sku']}，"
                        f"{error_item['message']}"
                    )
                )

            raise CommandError(
                (
                    "部分组合映射保存失败，"
                    f"失败数量：{result['failed']}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "元仓组合映射采集完成"
            )
        )