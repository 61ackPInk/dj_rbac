"""
-*- coding: utf-8 -*-
@File  : refresh_token.py
@Author: 61ackPink
@Time : 2026/9/11 16:41
@Desc : 刷新令牌
"""
import jwt
from django.conf import settings
from rest_framework import serializers

from apps.users.models import User


class RefreshTokenSerializer(serializers.Serializer):
    """刷新 Token 序列化器"""

    # 前端需要提交登录时获得的 refresh_token
    refresh_token = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """检查 refresh_token 是否有效"""

        refresh_token = attrs["refresh_token"]

        try:
            # 验证签名、过期时间并解析 Token
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[
                    settings.JWT_AUTH["ALGORITHM"]
                ],
            )
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError({
                "refresh_token": "刷新凭证已过期，请重新登录"
            })
        except jwt.InvalidTokenError:
            raise serializers.ValidationError({
                "refresh_token": "无效的刷新凭证"
            })

        # 这个接口只能接收 refresh_token
        # 防止用户使用 access_token 刷新
        if payload.get("token_type") != "refresh":
            raise serializers.ValidationError({
                "refresh_token": "凭证类型错误"
            })

        user_id = payload.get("user_id")

        if not user_id:
            raise serializers.ValidationError({
                "refresh_token": "刷新凭证缺少用户信息"
            })

        try:
            # 刷新 Token 时再次检查用户是否存在、是否启用
            user = User.objects.get(
                id=user_id,
                is_active=True,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "refresh_token": "用户不存在或已被禁用"
            })

        # 把用户对象交给视图，用于生成新的 access_token
        attrs["user"] = user

        return attrs