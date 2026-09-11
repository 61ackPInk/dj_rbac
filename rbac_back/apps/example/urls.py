"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/9/10 15:03
@Desc : 示例：路由
"""
from django.urls import path

from apps.example.views.example import ExampleAPIView

urlpatterns = [
    # 示例：example路由
    path('', ExampleAPIView.as_view(), name='example'),
]