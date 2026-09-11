"""
-*- coding: utf-8 -*-
@File  : login.py
@Author: 61ackPink
@Time : 2026/9/11 15:38
@Desc : 用户登录视图
"""
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserLoginSerializer
from common.utils.jwt import (
    create_access_token,
    create_refresh_token,
)
from django.utils import timezone

class UserLoginAPIView(GenericAPIView):
    """用户登录接口"""

    # 登录参数交给 UserLoginSerializer 校验
    serializer_class = UserLoginSerializer

    # 登录前用户还没有 Token，所以必须允许匿名访问
    permission_classes = [AllowAny]

    def post(self, request):
        """
        处理登录请求。

        请求数据示例：
        {
            "username": "admin",
            "password": "Admin@123456"
        }
        """

        # 将前端提交的数据传给登录序列化器
        serializer = self.get_serializer(data=request.data)

        # 验证用户名、密码和账号状态
        # 验证失败时，DRF 会自动返回 400 响应
        serializer.is_valid(raise_exception=True)

        # 登录序列化器验证成功后，
        # 会把查询到的用户对象放入 validated_data
        user = serializer.validated_data["user"]
        # 用户名和密码验证成功后，记录本次登录时间
        user.last_login = timezone.now()
        # 更新 last_login 字段
        user.save(update_fields=["last_login"])

        # 创建短期访问令牌
        access_token = create_access_token(user)
        # 创建长期刷新令牌
        refresh_token = create_refresh_token(user)

        # access_token 的有效秒数
        access_expires = (
            settings.JWT_AUTH["ACCESS_TOKEN_LIFETIME_MINUTES"]
            * 60
        )

        return Response({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": access_expires,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "last_login": user.last_login,
            },
        })

"""
前端提交用户名和密码
    ↓
UserLoginSerializer 验证账号
    ↓
获得 user 对象
    ↓
生成 access_token
    ↓
生成 refresh_token
    ↓
将 Token 和用户基本信息返回前端
"""