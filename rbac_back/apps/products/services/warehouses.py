"""
-*- coding: utf-8 -*-
@File  : warehouses.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 客户已开启仓库业务服务
"""

from apps.products.adapters import (
    BaseWarehouseProvider,
)
from apps.products.adapters.exceptions import (
    ProductProviderResponseError,
)


# ==================== 仓库业务服务 ====================


class WarehouseService:
    """获取并整理当前 ERP 的客户仓库。"""

    def __init__(
        self,
        warehouse_provider: (
            BaseWarehouseProvider
        ),
    ):
        """初始化仓库数据提供方。"""

        self.warehouse_provider = (
            warehouse_provider
        )

    # ==================== 仓库列表 ====================

    def get_warehouse_list(self) -> dict:
        """获取客户当前已开启的仓库列表。"""

        warehouses = (
            self.warehouse_provider
            .get_warehouse_list()
        )

        if not isinstance(warehouses, list):
            raise ProductProviderResponseError(
                "仓库 Provider 返回格式错误"
            )

        return {
            "items": warehouses,
        }