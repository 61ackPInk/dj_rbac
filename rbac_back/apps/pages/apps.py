"""
-*- coding: utf-8 -*-
@File  : apps.py
@Author: 61ackPink
@Time : 2026/9/16 14:53
@Desc :
"""
from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pages"
    verbose_name = "页面管理"