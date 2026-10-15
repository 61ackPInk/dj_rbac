"""
-*- coding: utf-8 -*-
@File  : crypto.py
@Author: 61ackPink
@Time : 2026/10/15 16:35
@Desc : 元仓网页请求 RSA 加密工具
"""

import base64

from cryptography.hazmat.primitives import (
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
)


# ==================== RSA 公钥加密 ====================


def encrypt_with_public_key(
        value: str,
        public_key: str,
) -> str:
    """
    使用 RSA 公钥加密字符串。

    加密方式与 JSEncrypt.encrypt() 一致：
    UTF-8 编码、PKCS#1 v1.5 填充、Base64 输出。
    """

    if not isinstance(value, str):
        raise ValueError(
            "RSA 加密内容必须是字符串"
        )

    if not public_key.strip():
        raise ValueError(
            "RSA 公钥不能为空"
        )

    try:
        loaded_key = (
            serialization.load_pem_public_key(
                public_key.encode("utf-8")
            )
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "RSA 公钥格式无效"
        ) from error

    if not isinstance(
            loaded_key,
            rsa.RSAPublicKey,
    ):
        raise ValueError(
            "配置内容不是 RSA 公钥"
        )

    try:
        encrypted_value = loaded_key.encrypt(
            value.encode("utf-8"),
            padding.PKCS1v15(),
        )
    except ValueError as error:
        raise ValueError(
            "RSA 加密失败，内容可能超过长度限制"
        ) from error

    return base64.b64encode(
        encrypted_value
    ).decode("ascii")
