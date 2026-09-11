"""
-*- coding: utf-8 -*-
@File  : user.py
@Author: 61ackPink
@Time : 2026/9/11 16:20
@Desc : 用户信息序列化器
"""
from rest_framework import serializers

from apps.users.models import Users


class UserInfoSerializer(serializers.ModelSerializer):
    """当前用户信息序列化器"""

    class Meta:
        model = Users

        # 只返回允许前端查看的字段
        # 密码绝对不能放在这里奥!!!!
        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "create_time",
            "last_login",
        ]

        # 这些字段只能读取，不能通过序列化器修改
        read_only_fields = fields