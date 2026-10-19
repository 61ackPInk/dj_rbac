"""
-*- coding: utf-8 -*-
@File  : base.py
@Author: 61ackPink
@Time : 2026/10/14 21:47
@Desc : 数据采集器抽象基类
"""

from abc import ABC, abstractmethod


class BaseCollector(ABC):
    """所有数据采集器必须遵循的基础接口。"""

    # ==================== 采集器信息 ====================

    @property
    @abstractmethod
    def source_name(self):
        """返回数据来源名称。"""

        raise NotImplementedError

    # ==================== 数据采集入口 ====================

    @abstractmethod
    def collect(self):
        """执行采集并返回标准化后的数据。"""

        raise NotImplementedError