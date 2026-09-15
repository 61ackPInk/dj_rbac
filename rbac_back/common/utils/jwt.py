"""
-*- coding: utf-8 -*-
@File  : jwt.py
@Author: 61ackPink
@Time : 2026/9/11 15:36
@Desc : 
"""
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt
from django.conf import settings


def create_token(user, token_type, lifetime):
    """
    创建 JWT。

    user:
        当前登录用户。

    token_type:
        Token 类型，目前有 access 和 refresh。

    lifetime:
        Token 的有效时长，使用 timedelta 表示。
    """

    # 使用 UTC 时间，避免不同时区造成过期时间判断错误
    now = datetime.now(timezone.utc)

    payload = {
        # 当前用户 ID
        "user_id": user.id,

        # 用户名不是身份查询的主要依据，
        # 放进 Token 主要用于调试或前端展示
        "username": user.username,

        # 区分 access_token 和 refresh_token
        "token_type": token_type,

        # Token 签发时间
        "iat": now,

        # Token 过期时间
        "exp": now + lifetime,

        # 每个 Token 的唯一编号
        "jti": str(uuid4()),
    }

    # 使用 Django 的 SECRET_KEY 对 Token 进行签名
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_AUTH["ALGORITHM"],
    )

    return token


def create_access_token(user):
    """创建短期访问令牌"""

    lifetime = timedelta(
        minutes=settings.JWT_AUTH[
            "ACCESS_TOKEN_LIFETIME_MINUTES"
        ]
    )

    return create_token(
        user=user,
        token_type="access",
        lifetime=lifetime,
    )


def create_refresh_token(user):
    """创建长期刷新令牌"""

    lifetime = timedelta(
        days=settings.JWT_AUTH[
            "REFRESH_TOKEN_LIFETIME_DAYS"
        ]
    )

    return create_token(
        user=user,
        token_type="refresh",
        lifetime=lifetime,
    )


# Token 内容示例
# {
#   "user_id": nth Stylized为bly，  kahe。  We need fix weird final? I accidentally glitch. Need continue coherent.
#   "username":fin "admin",
#   "token_type": "access",
#   "iat": 1789092000,
#   "exp": 1789093800,
#   "jti": "一个随机的唯一编号"
# }