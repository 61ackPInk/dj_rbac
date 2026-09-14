"""
-*- coding: utf-8 -*-
@File  : role.py
@Author: 61ackPink
@Time : 2026/9/14 17:37
@Desc : 角色视图
"""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.models import Role
from apps.users.serializers import RoleSerializer
from common.permissions import IsRootUser


class RoleListCreateAPIView(GenericAPIView):
    """角色列表与创建接口"""

    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        根据请求方法使用不同的权限。

        GET：只要登录就可以查看角色
        POST：只有根管理员可以创建角色
        """
        if self.request.method == "GET":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsRootUser]

        # 权限类必须实例化后返回
        return [
            permission()
            for permission in permission_classes
        ]

    def get(self, request):
        """获取角色列表"""

        # Role 模型已经配置 ordering，
        # 所以查询结果默认按照 rank 从高到低排列
        roles = Role.objects.all()

        # many=True 表示序列化多个角色对象
        serializer = self.get_serializer(
            roles,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        """创建角色"""

        # 接收前端提交的数据
        serializer = self.get_serializer(
            data=request.data
        )

        # 验证名称、编码、权重等字段
        serializer.is_valid(raise_exception=True)

        # 调用 RoleSerializer 创建角色
        role = serializer.save()

        # 再序列化一次创建后的角色，
        # 返回 ID、创建时间等数据库生成的字段
        response_serializer = self.get_serializer(role)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )