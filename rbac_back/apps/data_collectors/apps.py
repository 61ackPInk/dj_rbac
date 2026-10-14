"""
-*- coding: utf-8 -*-
@File  : apps.py
@Author: 61ackPink
@Time : 2026/10/14 18:11
@Desc : 数据采集系统应用配置
"""

from django.apps import AppConfig


class DataCollectorsConfig(AppConfig):
    """数据采集系统应用配置。"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.data_collectors"
    verbose_name = "数据采集系统"