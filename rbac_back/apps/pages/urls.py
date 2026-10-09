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
    PageRoleAssignAPIView,
    PageStatusUpdateAPIView,
    VisiblePageListAPIView,
)


urlpatterns = [
    # 当前用户可见页面
    #
    # 放在动态 ID 路由之前，
    # 使路由结构更加清晰
    path(
        "visible/",
        VisiblePageListAPIView.as_view(),
        name="page-visible-list",
    ),

    # GET：页面列表
    # POST：创建页面
    path(
        "",
        PageListCreateAPIView.as_view(),
        name="page-list-create",
    ),

    # GET：页面详情
    # PATCH：修改页面资料
    path(
        "<int:page_id>/",
        PageDetailAPIView.as_view(),
        name="page-detail",
    ),

    # PATCH：修改页面状态
    path(
        "<int:page_id>/status/",
        PageStatusUpdateAPIView.as_view(),
        name="page-status-update",
    ),

    # GET：查询页面可见角色
    # PATCH：替换页面可见角色
    path(
        "<int:page_id>/roles/",
        PageRoleAssignAPIView.as_view(),
        name="page-role-assign",
    ),
]
