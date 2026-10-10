"""
-*- coding: utf-8 -*-
@File  : base.py
@Author: 61ackPink
@Time : 2026/10/10 16:26
@Desc : 
"""
from abc import ABC, abstractmethod
from typing import Any


# ==================== ERP 商品适配器协议 ====================


class BaseProductProvider(ABC):
    """
    ERP 商品数据提供方统一协议。

    每个 ERP 适配器负责处理自身的鉴权、请求、分页和字段转换。
    商品业务层只依赖这里定义的能力，不直接依赖元仓。
    """

    # ==================== 普通商品 ====================

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
        product_id: str,
    ) -> dict[str, Any]:
        """获取普通商品详情。"""

        raise NotImplementedError

    # ==================== 组合商品 ====================

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