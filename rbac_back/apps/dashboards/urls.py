"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/10/9 18:30
@Desc : 
"""
from django.urls import path

from apps.dashboards.views.system_overview import SystemOverviewAPIView


urlpatterns = [
    # 仪表盘数据
    path(
        "system/overview/",
        SystemOverviewAPIView.as_view(),
        name="system-overview",
    ),
]
