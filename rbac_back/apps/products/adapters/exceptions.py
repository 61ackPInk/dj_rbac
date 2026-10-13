"""
-*- coding: utf-8 -*-
@File  : exceptions.py
@Author: 61ackPink
@Time : 2026/10/10 16:22
@Desc : ERP 调用和数据转换异常
"""
# ==================== ERP 适配器基础异常 ====================


class ProductProviderError(Exception):
    """商品系统访问 ERP 时发生的基础异常。"""


# ==================== ERP 配置异常 ====================


class ProductProviderConfigurationError(
    ProductProviderError
):
    """ERP 提供方或连接配置不正确。"""


# ==================== ERP 请求异常 ====================


class ProductProviderRequestError(
    ProductProviderError
):
    """请求 ERP 时发生网络、超时或远端服务异常。"""


# ==================== ERP 响应异常 ====================


class ProductProviderResponseError(
    ProductProviderError
):
    """ERP 响应成功，但返回内容不符合预期。"""