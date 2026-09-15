"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/11 16:20
@Desc : 用户信息序列化器
"""
from rest_framework import serializers

from apps.users.models import Role, User


class UserRoleInfoSerializer(serializers.ModelSerializer):
    """
    用户角色简要信息。

    这里只返回前端识别角色需要的字段，
    不返回角色创建时间等管理字段。
    """

    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "code",
            "rank",
        ]

        read_only_fields = fields


class UserInfoSerializer(serializers.ModelSerializer):
    """当前登录用户信息序列化器"""

    # 使用嵌套序列化器返回角色信息
    #
    # read_only=True 表示这个序列化器只负责展示，
    # 不能通过当前用户接口修改角色。
    role = UserRoleInfoSerializer(
        read_only=True,
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "is_active",
            "is_root",
            "role",
            "create_time",
            "last_login",
        ]

        # 当前序列化器只用于返回用户信息
        read_only_fields = fields