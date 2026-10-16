"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表接口视图
"""

import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.products.adapters.exceptions import (
    ProductProviderConfigurationError,
    ProductProviderError,
)
from apps.products.adapters.factory import (
    get_product_erp_provider_code,
    get_stock_provider,
)
from apps.products.serializers import (
    BundleListQuerySerializer,
    BundleListResponseSerializer,
)
from apps.products.services import BundleService
from common.permissions.operations import (
    HasOperationPermission,
)

from .products import (
    ProductProviderBadGateway,
    ProductProviderUnavailable,
)


logger = logging.getLogger(__name__)


# ==================== 组合商品列表接口 ====================


class BundleListAPIView(GenericAPIView):
    """查询本地组合资料及指定仓库实时库存。"""

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PRODUCT_BUNDLE_LIST",
    }

    query_serializer_class = (
        BundleListQuerySerializer
    )
    response_serializer_class = (
        BundleListResponseSerializer
    )

    def get(self, request, *args, **kwargs):
        """校验查询参数并返回组合商品列表。"""

        # ==================== 查询参数校验 ====================

        query_serializer = (
            self.query_serializer_class(
                data=request.query_params,
            )
        )
        query_serializer.is_valid(
            raise_exception=True
        )

        query = (
            query_serializer.to_service_query()
        )

        # ==================== 组合业务调用 ====================

        try:
            provider_code = (
                get_product_erp_provider_code()
            )

            service = BundleService(
                stock_provider=(
                    get_stock_provider()
                )
            )

            result = service.get_bundle_list(
                provider_code=provider_code,
                query=query,
            )
        except (
            ProductProviderConfigurationError
        ) as error:
            logger.exception(
                "组合商品数据源配置错误"
            )

            raise ProductProviderUnavailable() from error
        except ProductProviderError as error:
            logger.exception(
                "组合商品实时库存获取失败"
            )

            raise ProductProviderBadGateway() from error

        # ==================== 统一响应校验 ====================

        response_serializer = (
            self.response_serializer_class(
                data=result,
            )
        )

        if not response_serializer.is_valid():
            logger.error(
                "组合商品列表统一响应校验失败：%s",
                response_serializer.errors,
            )

            raise ProductProviderBadGateway()

        return Response(
            response_serializer.validated_data
        )