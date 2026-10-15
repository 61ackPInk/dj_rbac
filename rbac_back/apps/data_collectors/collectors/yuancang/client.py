"""
-*- coding: utf-8 -*-
@File  : client.py
@Author: 61ackPink
@Time : 2026/10/15 17:06
@Desc : 元仓网页数据采集客户端
"""

from typing import Any

import requests

from apps.data_collectors.collectors.exceptions import (
    CollectorAuthenticationError,
    CollectorRequestError,
    CollectorResponseError,
)
from apps.data_collectors.collectors.yuancang.config import (
    YuancangCollectorConfig,
)
from apps.data_collectors.collectors.yuancang.payloads import (
    build_login_payload,
)
from apps.data_collectors.collectors.yuancang.signing import (
    generate_request_sign,
)


class YuancangWebClient:
    """元仓网页数据采集请求客户端。"""

    def __init__(
        self,
        config: YuancangCollectorConfig,
        session=None,
    ):
        """初始化配置和 HTTP Session。"""

        self.config = config
        self.session = (
            session or requests.Session()
        )
        self.access_token = ""
        self.token_type = "Bearer"

    # ==================== 公共请求头 ====================

    def build_headers(
        self,
        payload: dict[str, Any],
        *,
        authenticated: bool,
    ) -> dict[str, str]:
        """构造元仓网页接口公共请求头。"""

        sign = generate_request_sign(
            payload,
            self.config.rsa_public_key,
        )

        if authenticated:
            if not self.access_token:
                raise CollectorAuthenticationError(
                    "尚未获取元仓网页登录Token"
                )

            authorization = (
                f"{self.token_type} "
                f"{self.access_token}"
            )
        else:
            authorization = "Bearer undefined"

        return {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "authorization": authorization,
            "devicename": (
                self.config.device_name
            ),
            "group": (
                self.config.request_group
            ),
            "paramtype": (
                self.config.param_type
            ),
            "prefix": (
                self.config.request_prefix
            ),
            "sign": sign,
            "version": "undefined",
        }

    # ==================== 基础 JSON 请求 ====================

    def _post_json(
        self,
        *,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        error_message: str,
    ) -> dict:
        """发送 POST 请求并解析 JSON 响应。"""

        try:
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=(
                    self.config.timeout_seconds
                ),
            )

            response.raise_for_status()
        except requests.RequestException as error:
            raise CollectorRequestError(
                error_message
            ) from error

        try:
            result = response.json()
        except ValueError as error:
            raise CollectorResponseError(
                "元仓网页接口响应不是有效JSON"
            ) from error

        if not isinstance(result, dict):
            raise CollectorResponseError(
                "元仓网页接口响应必须是对象"
            )

        return result

    # ==================== 网页登录 ====================

    def login(self) -> str:
        """模拟元仓网页登录并保存Token。"""

        payload = build_login_payload(
            username=self.config.username,
            password=self.config.password,
            device_name=(
                self.config.device_name
            ),
            public_key=(
                self.config.rsa_public_key
            ),
        )

        headers = self.build_headers(
            payload,
            authenticated=False,
        )

        result = self._post_json(
            url=self.config.login_url,
            payload=payload,
            headers=headers,
            error_message=(
                "元仓网页登录请求失败"
            ),
        )

        if result.get("state") != "000001":
            message = (
                result.get("msg")
                or "元仓网页登录失败"
            )

            raise CollectorAuthenticationError(
                message
            )

        data = result.get("data")

        if not isinstance(data, dict):
            raise CollectorResponseError(
                "元仓网页登录响应缺少data"
            )

        access_token = str(
            data.get("token") or ""
        ).strip()

        token_type = str(
            data.get("tokenType")
            or "Bearer"
        ).strip()

        if not access_token:
            raise CollectorResponseError(
                "元仓网页登录响应缺少token"
            )

        self.access_token = access_token
        self.token_type = token_type

        return access_token

    # ==================== 认证业务请求 ====================

    def post_authenticated(
        self,
        *,
        url: str,
        payload: dict[str, Any],
    ) -> dict:
        """发送需要网页登录认证的 POST 请求。"""

        if not self.access_token:
            self.login()

        headers = self.build_headers(
            payload,
            authenticated=True,
        )

        result = self._post_json(
            url=url,
            payload=payload,
            headers=headers,
            error_message=(
                "元仓网页业务请求失败"
            ),
        )

        if result.get("state") != "000001":
            message = (
                result.get("msg")
                or "元仓网页业务请求失败"
            )

            raise CollectorResponseError(
                message
            )

        return result

    # ==================== 组合映射列表 ====================

    def get_bundle_list_page(
        self,
        payload: dict[str, Any],
    ) -> dict:
        """请求一页元仓组合映射列表。"""

        return self.post_authenticated(
            url=self.config.bundle_list_url,
            payload=payload,
        )