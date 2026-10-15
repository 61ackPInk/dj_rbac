"""
-*- coding: utf-8 -*-
@File  : test_yuancang_client.py
@Author: 61ackPink
@Time : 2026/10/15 17:03
@Desc : 元仓网页数据采集客户端测试
"""

from unittest.mock import Mock

import requests
from django.test import SimpleTestCase

from apps.data_collectors.collectors.exceptions import (
    CollectorAuthenticationError,
    CollectorRequestError,
    CollectorResponseError,
)
from apps.data_collectors.collectors.yuancang.client import (
    YuancangWebClient,
)
from apps.data_collectors.collectors.yuancang.config import (
    YUANCANG_RSA_PUBLIC_KEY,
    YuancangCollectorConfig,
)


class YuancangWebClientTests(SimpleTestCase):
    """元仓网页数据采集客户端测试。"""

    def setUp(self):
        """初始化测试客户端。"""

        self.config = YuancangCollectorConfig(
            base_url=(
                "https://yc-client.anestcang.com"
            ),
            username="test-user",
            password="test-password",
            timeout_seconds=15,
            rsa_public_key=(
                YUANCANG_RSA_PUBLIC_KEY
            ),
        )

        self.session = Mock()
        self.client = YuancangWebClient(
            config=self.config,
            session=self.session,
        )

    def create_response(self, result):
        """创建模拟 HTTP 响应。"""

        response = Mock()
        response.json.return_value = result
        response.raise_for_status.return_value = None

        return response

    def test_login_saves_access_token(self):
        """登录成功后保存Token和类型。"""

        self.session.post.return_value = (
            self.create_response({
                "state": "000001",
                "msg": "登录成功",
                "data": {
                    "token": "test-token",
                    "tokenType": "Bearer",
                },
            })
        )

        result = self.client.login()

        self.assertEqual(
            result,
            "test-token",
        )
        self.assertEqual(
            self.client.access_token,
            "test-token",
        )
        self.assertEqual(
            self.client.token_type,
            "Bearer",
        )

        request_arguments = (
            self.session.post.call_args
        )

        request_payload = (
            request_arguments.kwargs["json"]
        )
        request_headers = (
            request_arguments.kwargs["headers"]
        )

        self.assertEqual(
            list(request_payload.keys()),
            [
                "username",
                "password",
                "deviceName",
            ],
        )
        self.assertNotEqual(
            request_payload["password"],
            "test-password",
        )
        self.assertEqual(
            request_headers["authorization"],
            "Bearer undefined",
        )
        self.assertTrue(
            request_headers["sign"]
        )
        self.assertEqual(
            request_arguments.kwargs["timeout"],
            15,
        )

    def test_authenticated_headers_use_token(
        self,
    ):
        """业务请求头使用登录Token。"""

        self.client.access_token = "test-token"

        headers = self.client.build_headers(
            {
                "page": 1,
                "prePage": 20,
            },
            authenticated=True,
        )

        self.assertEqual(
            headers["authorization"],
            "Bearer test-token",
        )
        self.assertEqual(
            headers["group"],
            "rpc-service-group-test",
        )
        self.assertTrue(headers["sign"])

    def test_login_business_error(self):
        """登录业务失败时抛出认证异常。"""

        self.session.post.return_value = (
            self.create_response({
                "state": "000403",
                "msg": "账号或密码错误",
                "data": {},
            })
        )

        with self.assertRaisesRegex(
            CollectorAuthenticationError,
            "账号或密码错误",
        ):
            self.client.login()

    def test_login_missing_token(self):
        """登录成功响应缺少Token时拒绝使用。"""

        self.session.post.return_value = (
            self.create_response({
                "state": "000001",
                "msg": "登录成功",
                "data": {},
            })
        )

        with self.assertRaisesRegex(
            CollectorResponseError,
            "缺少token",
        ):
            self.client.login()

    def test_login_request_error(self):
        """网络请求失败时转换为采集异常。"""

        self.session.post.side_effect = (
            requests.RequestException(
                "connection failed"
            )
        )

        with self.assertRaisesRegex(
            CollectorRequestError,
            "元仓网页登录请求失败",
        ):
            self.client.login()