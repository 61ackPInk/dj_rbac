"""
-*- coding: utf-8 -*-
@File  : bundle_mappings.py
@Author: 61ackPink
@Time : 2026/10/15
@Desc : 元仓组合映射采集配置
"""

import os
from dataclasses import dataclass
from datetime import date

from apps.data_collectors.collectors.exceptions import (
    CollectorConfigurationError,
)
from apps.data_collectors.collectors.yuancang.configs.common import (
    YuancangCommonConfig,
)


# ==================== 组合映射接口配置 ====================

YUANCANG_BUNDLE_MAPPING_LIST_PATH = (
    "/api/product/productMap/list"
)

DEFAULT_BUNDLE_PAGE_SIZE = 20


# ==================== 组合映射采集配置 ====================


@dataclass(frozen=True)
class YuancangBundleMappingConfig:
    """元仓组合映射采集专用配置。"""

    start_date: date
    page_size: int

    list_path: str = (
        YUANCANG_BUNDLE_MAPPING_LIST_PATH
    )

    # ==================== 配置加载 ====================

    @classmethod
    def from_environment(cls):
        """从应用环境变量加载组合采集配置。"""

        config = cls(
            start_date=cls._read_date(
                "YUANCANG_BUNDLE_COLLECTION_START_DATE"
            ),
            page_size=(
                cls._read_positive_integer(
                    "YUANCANG_BUNDLE_PAGE_SIZE",
                    DEFAULT_BUNDLE_PAGE_SIZE,
                )
            ),
        )

        return config

    # ==================== 接口地址 ====================

    def build_list_url(
        self,
        common_config: YuancangCommonConfig,
    ) -> str:
        """根据公共地址生成组合列表地址。"""

        return (
            f"{common_config.base_url}"
            f"{self.list_path}"
        )

    # ==================== 配置值解析 ====================

    @staticmethod
    def _read_positive_integer(
        variable_name: str,
        default_value: int,
    ) -> int:
        """读取大于零的整数配置。"""

        raw_value = os.getenv(
            variable_name,
            str(default_value),
        )

        try:
            value = int(raw_value)
        except ValueError as error:
            raise CollectorConfigurationError(
                f"{variable_name} 必须是整数"
            ) from error

        if value <= 0:
            raise CollectorConfigurationError(
                f"{variable_name} 必须大于零"
            )

        return value

    @staticmethod
    def _read_date(
        variable_name: str,
    ) -> date:
        """读取 YYYY-MM-DD 格式日期。"""

        raw_value = os.getenv(
            variable_name,
            "",
        ).strip()

        if not raw_value:
            raise CollectorConfigurationError(
                f"未配置 {variable_name}"
            )

        try:
            return date.fromisoformat(
                raw_value
            )
        except ValueError as error:
            raise CollectorConfigurationError(
                (
                    f"{variable_name} "
                    "必须使用 YYYY-MM-DD 格式"
                )
            ) from error