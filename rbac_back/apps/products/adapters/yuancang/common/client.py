"""
-*- coding: utf-8 -*-
@File  : client.py
@Author: 61ackPink
@Time : 2026/10/10 16:50
@Desc : 元仓开放平台公共请求客户端
"""
from typing import Any

import requests
from django.core.cache import cache

from apps.products.adapters.exceptions import (
    ProductProviderRequestError,
    ProductProviderResponseError,
)

from .config import YuanCangConfig
from .endpoints import YUANCANG_AUTH_PATH


# ==================== 元仓接口常量 ====================

YUANCANG_SUCCESS_STATE = "000001"
YUANCANG_UNAUTHORIZED_STATE = "000401"

YUANCANG_TOKEN_CACHE_KEY = (
    "products:yuancang:access-token"
)

# ==================== 元仓通用客户端 ====================


class YuanCangClient:
    """
    元仓开放平台 HTTP 客户端。

    负责：
    1. 获取并缓存 Token；
    2. 为业务请求添加 Authorization；
    3. 处理网络错误和元仓业务状态码；
    4. Token 失效时自动重新授权一次。
    """

    def __init__(
        self,
        config: YuanCangConfig | None = None,
    ):
        # 测试时可以传入独立配置，
        # 正常运行时从商品应用的 .env 加载
        self.config = (
            config
            or YuanCangConfig.from_environment()
        )

        # Session 会复用底层 HTTP 连接
        self.session = requests.Session()

    # ==================== 底层 POST 请求 ====================

    def _post(
        self,
        path: str,
        data: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """向元仓发送 POST 请求并解析 JSON。"""

        url = (
            f"{self.config.base_url}/"
            f"{path.lstrip('/')}"
        )

        try:
            response = self.session.post(
                url,
                json=data,
                headers=headers,
                timeout=(
                    self.config.timeout_seconds
                ),
            )

            response.raise_for_status()
        except requests.Timeout as error:
            raise ProductProviderRequestError(
                "请求元仓接口超时"
            ) from error
        except requests.RequestException as error:
            raise ProductProviderRequestError(
                "无法连接元仓接口"
            ) from error

        try:
            result = response.json()
        except ValueError as error:
            raise ProductProviderResponseError(
                "元仓接口没有返回有效 JSON"
            ) from error

        if not isinstance(result, dict):
            raise ProductProviderResponseError(
                "元仓接口返回格式错误"
            )

        return result

    # ==================== 获取授权 Token ====================

    def get_access_token(
        self,
        force_refresh: bool = False,
    ) -> dict[str, str]:
        """
        获取元仓授权信息。

        默认优先使用缓存；
        force_refresh=True 时重新请求授权接口。
        """

        if not force_refresh:
            cached_token = cache.get(
                YUANCANG_TOKEN_CACHE_KEY
            )

            if cached_token:
                return cached_token

        result = self._post(
            YUANCANG_AUTH_PATH,
            {
                "appKey": self.config.app_key,
                "appSecret": self.config.app_secret,
            },
        )

        if (
            result.get("state")
            != YUANCANG_SUCCESS_STATE
        ):
            raise ProductProviderResponseError(
                result.get("msg")
                or "元仓授权失败"
            )

        token_data = result.get("data")

        if not isinstance(token_data, dict):
            raise ProductProviderResponseError(
                "元仓授权响应缺少 data"
            )

        token = token_data.get("token")
        token_type = token_data.get(
            "tokenType"
        )

        if not token or not token_type:
            raise ProductProviderResponseError(
                "元仓授权响应缺少 Token"
            )

        auth_data = {
            "token": token,
            "token_type": token_type,
        }

        cache.set(
            YUANCANG_TOKEN_CACHE_KEY,
            auth_data,
            timeout=(
                self.config.token_cache_seconds
            ),
        )

        return auth_data

    # ==================== 发送业务请求 ====================

    def post(
        self,
        path: str,
        data: dict[str, Any],
    ) -> Any:
        """
        发送需要鉴权的元仓业务请求。

        元仓返回000401时清除缓存，
        重新获取 Token 后仅重试一次。
        """

        for attempt in range(2):
            auth_data = self.get_access_token(
                force_refresh=attempt > 0,
            )

            result = self._post(
                path,
                data,
                headers={
                    "Authorization": (
                        f"{auth_data['token_type']} "
                        f"{auth_data['token']}"
                    ),
                },
            )

            state = result.get("state")

            if (
                state
                == YUANCANG_UNAUTHORIZED_STATE
                and attempt == 0
            ):
                cache.delete(
                    YUANCANG_TOKEN_CACHE_KEY
                )
                continue

            if state != YUANCANG_SUCCESS_STATE:
                raise ProductProviderResponseError(
                    result.get("msg")
                    or "元仓接口请求失败"
                )

            return result.get("data")

        raise ProductProviderResponseError(
            "元仓授权失败，请稍后重试"
        )
