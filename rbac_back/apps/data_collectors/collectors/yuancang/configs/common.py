"""
-*- coding: utf-8 -*-
@File  : common.py
@Author: 61ackPink
@Time : 2026/10/15 16:42
@Desc : 元仓网页采集公共配置
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from apps.data_collectors.collectors.exceptions import (
    CollectorConfigurationError,
)


# ==================== 数据采集应用环境文件 ====================

DATA_COLLECTORS_APP_DIR = Path(
    __file__
).resolve().parents[3]

DATA_COLLECTORS_ENV_FILE = (
    DATA_COLLECTORS_APP_DIR / ".env"
)

# 系统环境变量优先于应用内的 .env 文件
load_dotenv(
    dotenv_path=DATA_COLLECTORS_ENV_FILE,
    override=False,
)


# ==================== 元仓接口路径 ====================

YUANCANG_LOGIN_PATH = (
    "/api/user/authorization/login"
)

# ==================== 元仓固定请求配置 ====================

YUANCANG_DEVICE_NAME = "Chrome"
YUANCANG_REQUEST_GROUP = (
    "rpc-service-group-test"
)
YUANCANG_PARAM_TYPE = "1"
YUANCANG_REQUEST_PREFIX = "com.yuancang"

DEFAULT_TIMEOUT_SECONDS = 15

# ==================== 元仓 RSA 公钥 ====================

YUANCANG_RSA_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA1MlgWuWiqOEMYUPkrR+B
JBDI6TiReZz4vQ0q9Y81d7LNK7vfmu8cGfwuvAw9aWjV6dW1ru0veHXMWwkgbd8W
x2pZSaC9mj4kolcYDV6NpnGYZD1bp4kmTQi0mdnuF5Zd06hLUrznewX8sb2tUfVH
ziAmdcNicYdRl3WQWiMWXNQL8kp9OpnD1+N22GPaIGC3hk9SIxHSbzQAoetTGBsx
qD/iDwicw49Ec1KMUzvMzVaf1i2K/1icCHxZp0RelMprbhvxcv9s3S0eyrTilRlc
oPU75U3cAeCp+hid2CG64Onz0Xu1P4pc5K/AOt64y2fcWED4sv1rcWto9s92ocI3
Mh/9w0Tk1Mn1wqgZgZnh8/AvAJKQcs/FvPQ3082nz/UGn/JWpibeASCBbfGxlwGh
2CZyVOtR4NNDwqn0Ysq/FvLdyiKMjHL01iEHHgtupHXgY9Qlro3apF5JiHU5jZN4
MW2odM2TyvSMP+rssQIeU2E7pZ+uGCQsOD5MvSQ46k+cHTgk69eS5SghEKfM1j9T
+wsesVNFRQCTgAh283JD0nzMThYPWJeiavei7pE3oVyq4g/0aWMZmm15IlV57w2d
IBkwZp5oqQVOaUkBQJfYxGTtykMV+7gnc2PNnxGCoUQyqU/ICcbWmvZWxCVNX+YM
dWxVDPljqwSNc6jH3RqNfpMCAwEAAQ==
-----END PUBLIC KEY-----"""


# ==================== 元仓采集配置对象 ====================


@dataclass(frozen=True)
class YuancangCommonConfig:
    """元仓网页采集公共连接配置。"""

    base_url: str
    username: str
    password: str
    timeout_seconds: int

    rsa_public_key: str = (
        YUANCANG_RSA_PUBLIC_KEY
    )
    device_name: str = YUANCANG_DEVICE_NAME
    request_group: str = (
        YUANCANG_REQUEST_GROUP
    )
    param_type: str = YUANCANG_PARAM_TYPE
    request_prefix: str = (
        YUANCANG_REQUEST_PREFIX
    )

    # ==================== 配置加载 ====================

    @classmethod
    def from_environment(cls):
        """从环境变量加载元仓采集配置。"""

        config = cls(
            base_url=os.getenv(
                "YUANCANG_COLLECTOR_BASE_URL",
                "",
            ).strip().rstrip("/"),
            username=os.getenv(
                "YUANCANG_COLLECTOR_USERNAME",
                "",
            ).strip(),
            password=os.getenv(
                "YUANCANG_COLLECTOR_PASSWORD",
                "",
            ),
            timeout_seconds=(
                cls._read_positive_integer(
                    "YUANCANG_COLLECTOR_TIMEOUT_SECONDS",
                    DEFAULT_TIMEOUT_SECONDS,
                )
            ),
        )

        config.validate()

        return config

    # ==================== 接口地址 ====================

    @property
    def login_url(self) -> str:
        """返回元仓网页登录地址。"""

        return (
            f"{self.base_url}"
            f"{YUANCANG_LOGIN_PATH}"
        )

    # ==================== 数值配置解析 ====================

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

    # ==================== 必填配置检查 ====================

    def validate(self):
        """检查元仓采集必填配置。"""

        if not self.base_url:
            raise CollectorConfigurationError(
                "未配置元仓网页地址"
            )

        if not self.username:
            raise CollectorConfigurationError(
                "未配置元仓登录账号"
            )

        if not self.password:
            raise CollectorConfigurationError(
                "未配置元仓登录密码"
            )