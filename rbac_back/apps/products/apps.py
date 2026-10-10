"""
-*- coding: utf-8 -*-
@File  : apps.py
@Author: 61ackPink
@Time : 2026/10/10 16:01
@Desc : 
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """商品系统应用配置。"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    verbose_name = "商品系统"