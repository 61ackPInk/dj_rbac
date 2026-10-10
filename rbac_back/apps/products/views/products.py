"""
-*- coding: utf-8 -*-
@File  : products.py
@Author: 61ackPink
@Time : 2026/10/10 17:16
@Desc : 普通商品列表与详情接口视图
"""

import logging

from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.products.adapters.exceptions import (
    ProductProviderConfigurationError,
    ProductProviderError,
)
from apps.products.adapters.factory import (
    get_product_provider,
)
from apps.products.serializers import (
    ProductListQuerySerializer,
    ProductListResponseSerializer,
)
from apps.products.services import ProductService
from common.permissions.operations import (
    HasOperationPermission,
)


logger = logging.getLogger(__name__)


# ==================== 商品数据源异常 ====================


class ProductProviderUnavailable(APIException):
    """商品数据源配置不可用。"""

    status_code = 503
    default_detail = "商品数据源暂时不可用"
    default_code = "product_provider_unavailable"


class ProductProviderBadGateway(APIException):
    """第三方商品数据接口请求失败。"""

    status_code = 502
    default_detail = "商品数据获取失败，请稍后重试"
    default_code = "product_provider_bad_gateway"


# ==================== 商品列表接口 ====================


class ProductListAPIView(GenericAPIView):
    """查询当前 ERP 中的普通商品列表。"""

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "PRODUCT_LIST",
    }

    query_serializer_class = (
        ProductListQuerySerializer
    )
    response_serializer_class = (
        ProductListResponseSerializer
    )

    def get(self, request, *args, **kwargs):
        """校验查询条件并返回统一商品列表。"""

        # --------------------
        # 校验前端查询参数
        # --------------------

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

        # --------------------
        # 调用商品服务层
        # --------------------

        try:
            service = ProductService(
                get_product_provider()
            )
            result = service.get_product_list(
                query
            )
        except (
            ProductProviderConfigurationError
        ) as error:
            logger.exception(
                "商品数据源配置错误"
            )

            raise ProductProviderUnavailable() from error
        except ProductProviderError as error:
            logger.exception(
                "第三方商品接口请求失败"
            )

            raise ProductProviderBadGateway() from error

        # --------------------
        # 校验统一响应结构
        # --------------------

        response_serializer = (
            self.response_serializer_class(
                data=result,
            )
        )

        if not response_serializer.is_valid():
            logger.error(
                "商品列表统一响应校验失败：%s",
                response_serializer.errors,
            )

            raise ProductProviderBadGateway()

        # 项目自定义 Renderer 会统一包装
        # code、message 和 data
        return Response(
            response_serializer.validated_data
        )