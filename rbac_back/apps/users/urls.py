"""
-*- coding: utf-8 -*-
@File  : urls.py
@Author: 61ackPink
@Time : 2026/9/10 16:58
@Desc : 用户功能API
"""
from django.urls import path

from apps.users.views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    CurrentUserAPIView,
)

# 接口
urlpatterns = [
    # 用户注册
    path(
        "register/",
        UserRegisterAPIView.as_view(),
        name="user-register",
    ),
    # 用户登录
    path(
        "login/",
        UserLoginAPIView.as_view(),
        name="user-login",
    ),
    # 用户信息
    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    )
]