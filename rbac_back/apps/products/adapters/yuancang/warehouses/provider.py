"""
-*- coding: utf-8 -*-
@File  : provider.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 元仓客户已开启仓库数据适配器
"""

from typing import Any

from apps.products.adapters import (
    BaseWarehouseProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)

from ..common.client import YuanCangClient
from .endpoints import (
    YUANCANG_CUSTOMER_WAREHOUSE_PATH,
)
from .mappers import map_warehouse_item


# ==================== 元仓仓库适配器 ====================


class YuanCangWarehouseProvider(
    BaseWarehouseProvider
):
    """读取并转换客户在元仓已开启的仓库。"""

    def __init__(
        self,
        client: YuanCangClient | None = None,
    ):
        """初始化元仓公共客户端。"""

        self.client = (
            client or YuanCangClient()
        )

    # ==================== 仓库列表 ====================

    def get_warehouse_list(
        self,
    ) -> list[dict[str, Any]]:
        """获取客户当前已开启的仓库列表。"""

        source_data = self.client.post(
            YUANCANG_CUSTOMER_WAREHOUSE_PATH,
            {},
        )

        if not isinstance(source_data, list):
            raise ProductProviderResponseError(
                "元仓客户仓库响应 data 必须是列表"
            )

        return [
            map_warehouse_item(source_item)
            for source_item in source_data
            if isinstance(source_item, dict)
        ]