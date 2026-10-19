"""
-*- coding: utf-8 -*-
@File  : test_yuancang_payloads.py
@Author: 61ackPink
@Time : 2026/10/15 16:58
@Desc : 元仓网页登录请求体测试
"""

import base64

from cryptography.hazmat.primitives import (
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import (
    padding,
    rsa,
)
from django.test import SimpleTestCase

from apps.data_collectors.collectors.yuancang.security.payloads import (
    build_login_payload,
)


class YuancangPayloadTests(SimpleTestCase):
    """元仓网页请求体构造测试。"""

    @classmethod
    def setUpClass(cls):
        """生成测试专用 RSA 密钥。"""

        super().setUpClass()

        cls.private_key = (
            rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
        )

        cls.public_key = (
            cls.private_key
            .public_key()
            .public_bytes(
                encoding=(
                    serialization.Encoding.PEM
                ),
                format=(
                    serialization
                    .PublicFormat
                    .SubjectPublicKeyInfo
                ),
            )
            .decode("utf-8")
        )

    def test_build_login_payload(self):
        """正确构造元仓登录请求体。"""

        result = build_login_payload(
            username="test-user",
            password="test-password",
            device_name="Chrome",
            public_key=self.public_key,
        )

        self.assertEqual(
            result["username"],
            "test-user",
        )
        self.assertEqual(
            result["deviceName"],
            "Chrome",
        )
        self.assertNotEqual(
            result["password"],
            "test-password",
        )

    def test_password_can_be_decrypted(self):
        """加密密码可由对应测试私钥解密。"""

        result = build_login_payload(
            username="test-user",
            password="test-password",
            device_name="Chrome",
            public_key=self.public_key,
        )

        decrypted_password = (
            self.private_key.decrypt(
                base64.b64decode(
                    result["password"]
                ),
                padding.PKCS1v15(),
            )
            .decode("utf-8")
        )

        self.assertEqual(
            decrypted_password,
            "test-password",
        )

    def test_login_field_order_is_fixed(self):
        """登录请求字段顺序与网页保持一致。"""

        result = build_login_payload(
            username="test-user",
            password="test-password",
            device_name="Chrome",
            public_key=self.public_key,
        )

        self.assertEqual(
            list(result.keys()),
            [
                "username",
                "password",
                "deviceName",
            ],
        )

    def test_empty_password_raises_error(self):
        """空密码不能用于构造登录请求。"""

        with self.assertRaisesRegex(
            ValueError,
            "元仓登录密码不能为空",
        ):
            build_login_payload(
                username="test-user",
                password="",
                device_name="Chrome",
                public_key=self.public_key,
            )
