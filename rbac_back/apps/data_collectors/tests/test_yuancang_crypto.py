"""
-*- coding: utf-8 -*-
@File  : test_yuancang_crypto.py
@Author: 61ackPink
@Time : 2026/10/15 16:38
@Desc : 元仓网页请求 RSA 加密工具测试
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

from apps.data_collectors.collectors.yuancang.crypto import (
    encrypt_with_public_key,
)


class YuancangCryptoTests(SimpleTestCase):
    """元仓 RSA 加密工具测试。"""

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

    def test_encrypted_value_can_be_decrypted(
        self,
    ):
        """加密结果可以使用对应私钥解密。"""

        source_value = "测试密码123"

        encrypted_value = (
            encrypt_with_public_key(
                source_value,
                self.public_key,
            )
        )

        encrypted_bytes = base64.b64decode(
            encrypted_value
        )

        decrypted_value = (
            self.private_key.decrypt(
                encrypted_bytes,
                padding.PKCS1v15(),
            )
            .decode("utf-8")
        )

        self.assertEqual(
            decrypted_value,
            source_value,
        )

    def test_result_is_rsa_base64_value(self):
        """加密结果是标准Base64字符串。"""

        encrypted_value = (
            encrypt_with_public_key(
                "password",
                self.public_key,
            )
        )

        encrypted_bytes = base64.b64decode(
            encrypted_value,
            validate=True,
        )

        # 2048位RSA密文固定为256字节
        self.assertEqual(
            len(encrypted_bytes),
            256,
        )

    def test_same_value_has_different_ciphertext(
        self,
    ):
        """PKCS#1填充使相同内容产生不同密文。"""

        first_value = encrypt_with_public_key(
            "password",
            self.public_key,
        )

        second_value = encrypt_with_public_key(
            "password",
            self.public_key,
        )

        self.assertNotEqual(
            first_value,
            second_value,
        )

    def test_invalid_public_key_raises_error(
        self,
    ):
        """无效公钥会抛出明确异常。"""

        with self.assertRaisesRegex(
            ValueError,
            "RSA 公钥格式无效",
        ):
            encrypt_with_public_key(
                "password",
                "invalid-public-key",
            )