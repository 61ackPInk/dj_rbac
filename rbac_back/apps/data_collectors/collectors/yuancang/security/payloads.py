"""
-*- coding: utf-8 -*-
@File  : payloads.py
@Author: 61ackPink
@Time : 2026/10/15 16:56
@Desc : 元仓网页请求体构造
"""

from apps.data_collectors.collectors.yuancang.security.crypto import (
    encrypt_with_public_key,
)


# ==================== 登录请求体 ====================


def build_login_payload(
        *,
        username: str,
        password: str,
        device_name: str,
        public_key: str,
) -> dict:
    """
    构造元仓网页登录请求体。

    字段顺序必须与元仓网页保持一致：
    username、password、deviceName。
    """

    if not username:
        raise ValueError(
            "元仓登录账号不能为空"
        )

    if not password:
        raise ValueError(
            "元仓登录密码不能为空"
        )

    if not device_name:
        raise ValueError(
            "元仓登录设备名称不能为空"
        )

    encrypted_password = (
        encrypt_with_public_key(
            password,
            public_key,
        )
    )

    return {
        "username": username,
        "password": encrypted_password,
        "deviceName": device_name,
    }
