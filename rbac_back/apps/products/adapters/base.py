"""
-*- coding: utf-8 -*-
@File  : base.py
@Author: 61ackPink
@Time : 2026/10/10 16:26
@Desc :
"""
from abc import ABC, abstractmethod
from typing import Any


# ==================== 普通商品适配器协议 ====================


class BaseProductProvider(ABC):
    """
    ERP 普通商品数据提供方协议。

    具体 ERP 负责处理自身的请求和字段转换，
    商品服务层只依赖这里定义的统一能力。
    """

    @abstractmethod
    def get_product_list(
            self,
            query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取普通商品列表。"""

        raise NotImplementedError

    @abstractmethod
    def get_product_detail(
            self,
            customer_sku: str,
    ) -> dict[str, Any]:
        """根据客户 SKU 获取普通商品详情。"""

        raise NotImplementedError


# ==================== 商品库存适配器协议 ====================


class BaseStockProvider(ABC):
    """ERP 商品库存数据提供方协议。"""

    @abstractmethod
    def get_stock_list(
            self,
            warehouse_code: str,
            customer_skus: list[str],
    ) -> dict[str, dict[str, Any]]:
        """
        批量获取指定仓库的商品库存。

        返回值以 customer_sku 作为键，
        方便商品服务层快速合并库存。
        """

        raise NotImplementedError


# ==================== 组合商品适配器协议 ====================


class BaseBundleProvider(ABC):
    """
    ERP 组合商品数据提供方协议。

    组合商品接口与普通商品接口相互独立，
    避免尚未接入组合 API 时阻塞普通商品开发。
    """

    @abstractmethod
    def get_bundle_list(
            self,
            query: dict[str, Any],
    ) -> dict[str, Any]:
        """获取组合商品列表。"""

        raise NotImplementedError

    @abstractmethod
    def get_bundle_detail(
            self,
            bundle_id: str,
    ) -> dict[str, Any]:
        """获取组合商品详情。"""

        raise NotImplementedError
