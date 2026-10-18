"""
-*- coding: utf-8 -*-
@File  : bundles.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 组合商品列表接口视图
"""

import logging

from django.http import Http404
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
    BundleDetailPathSerializer,
    BundleDetailQuerySerializer,
    BundleDetailResponseSerializer,
    BundleListQuerySerializer,
    BundleListResponseSerializer,
)
from apps.products.services import BundleService
from apps.products.models import ProductBundle
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


# ==================== 组合商品详情接口 ====================


class BundleDetailAPIView(GenericAPIView):
    """查询组合组成资料及指定仓库实时库存。"""

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PRODUCT_BUNDLE_DETAIL",
    }

    path_serializer_class = (
        BundleDetailPathSerializer
    )
    query_serializer_class = (
        BundleDetailQuerySerializer
    )
    response_serializer_class = (
        BundleDetailResponseSerializer
    )

    def get(
        self,
        request,
        bundle_id,
        *args,
        **kwargs,
    ):
        """校验组合ID和仓库后返回组合详情。"""

        # ==================== 路径参数校验 ====================

        path_serializer = (
            self.path_serializer_class(
                data={
                    "bundle_id": bundle_id,
                }
            )
        )
        path_serializer.is_valid(
            raise_exception=True
        )

        validated_bundle_id = (
            path_serializer.validated_data[
                "bundle_id"
            ]
        )

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

        # ==================== 组合详情业务调用 ====================

        try:
            provider_code = (
                get_product_erp_provider_code()
            )

            service = BundleService(
                stock_provider=(
                    get_stock_provider()
                )
            )

            result = service.get_bundle_detail(
                provider_code=provider_code,
                bundle_id=validated_bundle_id,
                query=query,
            )
        except ProductBundle.DoesNotExist as error:
            raise Http404(
                "组合商品不存在"
            ) from error
        except (
            ProductProviderConfigurationError
        ) as error:
            logger.exception(
                "组合商品详情数据源配置错误"
            )

            raise ProductProviderUnavailable() from error
        except ProductProviderError as error:
            logger.exception(
                "组合商品详情实时库存获取失败"
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
                "组合商品详情统一响应校验失败：%s",
                response_serializer.errors,
            )

            raise ProductProviderBadGateway()

        return Response(
            response_serializer.validated_data
        )
