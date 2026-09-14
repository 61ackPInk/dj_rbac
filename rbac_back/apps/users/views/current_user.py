"""
-*- coding: utf-8 -*-
@File  : current_user.py
@Author: 61ackPink
@Time : 2026/9/11 16:22
@Desc : 当前用户信息视图
"""
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import UserInfoSerializer


class CurrentUserAPIView(GenericAPIView):
    """获取当前登录用户信息"""

    serializer_class = UserInfoSerializer

    # 明确要求当前接口必须登录
    # 即使 settings.py 已经全局配置，这里写出来也更直观
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        JWTAuthentication 验证成功后，会自动设置：

        request.user：当前用户对象
        request.auth：当前请求携带的 Token
        """

        # 将当前用户对象转换成可以返回的字典数据
        serializer = self.get_serializer(request.user)

        return Response(serializer.data)