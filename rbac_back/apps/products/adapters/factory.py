"""
-*- coding: utf-8 -*-
@File  : factory.py
@Author: 61ackPink
@Time : 2026/10/10 17:09
@Desc : 根据商品系统配置选择对应的ERP数据适配器
"""

import os
from functools import lru_cache

from apps.products.adapters.base import (
    BaseProductProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderConfigurationError,
)
from apps.products.adapters.yuancang import (
    YuanCangProductProvider,
)

# 导入元仓配置模块时会加载商品应用目录下的 .env
from apps.products.adapters.yuancang.config import (
    PRODUCTS_ENV_FILE,
)


# ==================== 普通商品 Provider 工厂 ====================


@lru_cache(maxsize=1)
def get_product_provider() -> BaseProductProvider:
    """
    获取当前启用的普通商品 Provider。

    使用缓存复用 Provider 内部的 requests.Session，
    避免每次请求都重新建立客户端对象。
    """

    # PRODUCTS_ENV_FILE 已在配置模块中加载。
    # 这里引用一次，明确当前配置来源于商品应用。
    _ = PRODUCTS_ENV_FILE

    provider_code = os.getenv(
        "PRODUCT_ERP_PROVIDER",
        "",
    ).strip().lower()

    if provider_code == "yuancang":
        return YuanCangProductProvider()

    if not provider_code:
        raise ProductProviderConfigurationError(
            "未配置商品 ERP 提供方"
        )

    raise ProductProviderConfigurationError(
        f"不支持的商品 ERP 提供方：{provider_code}"
    )
