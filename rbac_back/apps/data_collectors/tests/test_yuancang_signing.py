"""
-*- coding: utf-8 -*-
@File  : test_yuancang_signing.py
@Author: 61ackPink
@Time : 2026/10/15 16:47
@Desc : 元仓网页请求动态签名测试
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

from apps.data_collectors.collectors.yuancang.signing import (
    build_signature_source,
    generate_request_sign,
)


class YuancangSigningTests(SimpleTestCase):
    """元仓动态签名生成测试。"""

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

    def test_build_login_signature_source(self):
        """登录参数按原始字段顺序生成原文。"""

        payload = {
            "username": "test-user",
            "password": "test-password",
            "deviceName": "Chrome",
        }

        result = build_signature_source(
            payload,
            1792042435000,
        )

        self.assertEqual(
            result,
            (
                "username|password|deviceName"
                "|_t&1792042435000"
            ),
        )

    def test_none_value_is_excluded(self):
        """值为None的字段不会参与签名。"""

        payload = {
            "username": "test-user",
            "captcha": None,
            "deviceName": "Chrome",
        }

        result = build_signature_source(
            payload,
            1792042435000,
        )

        self.assertEqual(
            result,
            (
                "username|deviceName"
                "|_t&1792042435000"
            ),
        )

        # 生成签名不能修改调用方传入的数据
        self.assertIn(
            "captcha",
            payload,
        )

    def test_generated_sign_contains_expected_source(
        self,
    ):
        """RSA sign 解密后是预期签名原文。"""

        payload = {
            "page": 1,
            "prePage": 20,
        }

        encrypted_sign = generate_request_sign(
            payload,
            self.public_key,
            timestamp_ms=1792042435000,
        )

        decrypted_sign = (
            self.private_key.decrypt(
                base64.b64decode(
                    encrypted_sign
                ),
                padding.PKCS1v15(),
            )
            .decode("utf-8")
        )

        self.assertEqual(
            decrypted_sign,
            (
                "page|prePage"
                "|_t&1792042435000"
            ),
        )

    def test_invalid_payload_raises_error(self):
        """非字典请求参数不能用于签名。"""

        with self.assertRaisesRegex(
            ValueError,
            "签名请求参数必须是字典",
        ):
            build_signature_source(
                [],
                1792042435000,
            )