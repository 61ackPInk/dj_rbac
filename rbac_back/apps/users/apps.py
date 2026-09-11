"""
-*- coding: utf-8 -*-
@File  : apps.py
@Author: 61ackPink
@Time : 2026/9/10 16:58
@Desc : 
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "用户管理"