"""
-*- coding: utf-8 -*-
@File  : warehouses.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 客户已开启仓库接口视图
"""

import logging

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.products.adapters.exceptions import (
    ProductProviderConfigurationError,
    ProductProviderError,
)
from apps.products.adapters.factory import (
    get_warehouse_provider,
)
from apps.products.serializers import (
    WarehouseListResponseSerializer,
)
from apps.products.services import (
    WarehouseService,
)
from common.permissions.operations import (
    HasOperationPermission,
)

from .products import (
    ProductProviderBadGateway,
    ProductProviderUnavailable,
)


logger = logging.getLogger(__name__)


# ==================== 仓库列表接口 ====================


class WarehouseListAPIView(GenericAPIView):
    """获取当前 ERP 账号已经开启的仓库。"""

    permission_classes = [
        HasOperationPermission,
    ]

    # 商品列表和商品组合都会使用仓库筛选，
    # 因此拥有其中任意一个页面权限即可访问
    required_permissions = {
        "GET": [
            "PRODUCT_LIST",
            "PRODUCT_BUNDLE_LIST",
        ],
    }

    response_serializer_class = (
        WarehouseListResponseSerializer
    )

    def get(self, request, *args, **kwargs):
        """获取并返回统一仓库列表。"""

        # --------------------
        # 调用仓库业务服务
        # --------------------

        try:
            service = WarehouseService(
                warehouse_provider=(
                    get_warehouse_provider()
                ),
            )

            result = (
                service.get_warehouse_list()
            )
        except (
            ProductProviderConfigurationError
        ) as error:
            logger.exception(
                "仓库数据源配置错误"
            )

            raise ProductProviderUnavailable() from error

        except ProductProviderError as error:
            logger.exception(
                "第三方仓库接口请求失败"
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
                "仓库列表统一响应校验失败：%s",
                response_serializer.errors,
            )

            raise ProductProviderBadGateway()

        # 项目自定义 Renderer 会统一包装
        # code、message 和 data
        return Response(
            response_serializer.validated_data
        )