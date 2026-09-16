"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/9/16 16:59
@Desc : 页面路由
"""
from django.urls import path

from apps.pages.views import (
    PageDetailAPIView,
    PageListCreateAPIView,
    VisiblePageListAPIView,
)

urlpatterns = [
    # 页面列表和创建
    path(
        "",
        PageListCreateAPIView.as_view(),
        name="page-list-create",
    ),

    # 页面详情、修改和停用
    path(
        "<int:page_id>/",
        PageDetailAPIView.as_view(),
        name="page-detail",
    ),

    # 当前用户可见页面
    path(
        "visible/",
        VisiblePageListAPIView.as_view(),
        name="page-visible-list",
    ),
]
