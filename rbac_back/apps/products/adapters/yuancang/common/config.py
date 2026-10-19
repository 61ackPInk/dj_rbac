"""
-*- coding: utf-8 -*-
@File  : config.py
@Author: 61ackPink
@Time : 2026/10/10 16:41
@Desc : 元仓开放平台公共连接配置
"""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from apps.products.adapters.exceptions import (
    ProductProviderConfigurationError,
)


# ==================== 商品应用环境文件 ====================

PRODUCTS_APP_DIR = Path(
    __file__
).resolve().parents[3]

PRODUCTS_ENV_FILE = (
    PRODUCTS_APP_DIR / ".env"
)

# 系统环境变量优先级高于应用内的 .env 文件
load_dotenv(
    dotenv_path=PRODUCTS_ENV_FILE,
    override=False,
)


# ==================== 元仓默认请求配置 ====================

DEFAULT_TOKEN_CACHE_SECONDS = 12 * 60 * 60
DEFAULT_TIMEOUT_SECONDS = 15


# ==================== 元仓配置对象 ====================


@dataclass(frozen=True)
class YuanCangConfig:
    """元仓开放平台连接配置。"""

    base_url: str
    app_key: str
    app_secret: str
    token_cache_seconds: int
    timeout_seconds: int

    # ==================== 加载配置 ====================

    @classmethod
    def from_environment(cls):
        """
        从系统环境变量或商品应用 .env 文件加载配置。

        系统环境变量优先，
        应用目录内的 .env 作为本地开发配置。
        """

        config = cls(
            base_url=os.getenv(
                "YUANCANG_API_BASE_URL",
                "",
            ).strip().rstrip("/"),
            app_key=os.getenv(
                "YUANCANG_APP_KEY",
                "",
            ).strip(),
            app_secret=os.getenv(
                "YUANCANG_APP_SECRET",
                "",
            ).strip(),
            token_cache_seconds=(
                cls._read_positive_integer(
                    "YUANCANG_TOKEN_CACHE_SECONDS",
                    DEFAULT_TOKEN_CACHE_SECONDS,
                )
            ),
            timeout_seconds=(
                cls._read_positive_integer(
                    "YUANCANG_TIMEOUT_SECONDS",
                    DEFAULT_TIMEOUT_SECONDS,
                )
            ),
        )

        config.validate()

        return config

    # ==================== 数值配置解析 ====================

    @staticmethod
    def _read_positive_integer(
        variable_name: str,
        default_value: int,
    ) -> int:
        """读取大于0的整数配置。"""

        raw_value = os.getenv(
            variable_name,
            str(default_value),
        )

        try:
            value = int(raw_value)
        except ValueError as error:
            raise ProductProviderConfigurationError(
                f"{variable_name} 必须是整数"
            ) from error

        if value <= 0:
            raise ProductProviderConfigurationError(
                f"{variable_name} 必须大于0"
            )

        return value

    # ==================== 必填配置检查 ====================

    def validate(self):
        """检查元仓连接必填配置。"""

        if not self.base_url:
            raise ProductProviderConfigurationError(
                "未配置元仓 API 地址"
            )

        if not self.app_key:
            raise ProductProviderConfigurationError(
                "未配置元仓 APP Key"
            )

        if not self.app_secret:
            raise ProductProviderConfigurationError(
                "未配置元仓 APP Secret"
            )