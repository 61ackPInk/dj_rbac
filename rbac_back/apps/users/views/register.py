"""
-*- coding: utf-8 -*-
@File  : register.py
@Author: 61ackPink
@Time : 2026/9/11 14:36
@Desc : 用户注册视图
"""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import UserRegisterSerializer
from common.utils.log import log


class UserRegisterAPIView(GenericAPIView):
    """用户注册接口"""
    # 使用用户注册的序列化器
    serializer_class = UserRegisterSerializer

    # AllowAny 表示不需要登录也能访问
    # 注册前用户还没有账号，因此注册接口必须允许匿名访问
    permission_classes = [AllowAny]

    def post(self, request):
        """
        request.data = 前端提交的数据
        """

        # 把前端提交的数据交给注册序列化器
        serializer = self.get_serializer(data=request.data)
        # 执行序列化器中的所有验证
        # raise_exception=True 验证失败时直接返回 400
        serializer.is_valid(raise_exception=True)

        # 调用序列化器的 create() 方法创建用户
        user = serializer.save()

        # 日志：注册成功
        log.info(f'用户：{user.username}-注册成功！')

        # 注册成功后返回安全的用户信息
        # 不返回 password，即使数据库里保存的是加密密码也不应该返回
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )