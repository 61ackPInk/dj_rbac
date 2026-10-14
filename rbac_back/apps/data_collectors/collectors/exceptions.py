"""
-*- coding: utf-8 -*-
@File  : exceptions.py
@Author: 61ackPink
@Time : 2026/10/14 21:47
@Desc : 数据采集器异常定义
"""


class DataCollectorError(Exception):
    """数据采集器异常基类。"""


class CollectorConfigurationError(DataCollectorError):
    """采集器配置错误。"""


class CollectorAuthenticationError(DataCollectorError):
    """采集目标身份认证失败。"""


class CollectorRequestError(DataCollectorError):
    """采集请求发送失败。"""


class CollectorResponseError(DataCollectorError):
    """采集响应内容异常。"""