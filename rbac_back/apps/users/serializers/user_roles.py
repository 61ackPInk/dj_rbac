"""
-*- coding: utf-8 -*-
@File  : user_roles.py
@Author: 61ackPink
@Time : 2026/9/15 14:47
@Desc : 用户角色分配
"""
from rest_framework import serializers

from apps.users.models import Role, User


class UserRoleAssignSerializer(serializers.ModelSerializer):
    """给用户分配单个角色"""

    role_id = serializers.PrimaryKeyRelatedField(
        # 只能分配当前处于启用状态的角色
        queryset=Role.objects.filter(is_active=True),

        # 前端提交 role_id，
        # 保存时实际修改 User.role 字段
        source="role",

        # role_id 只用于接收请求，不直接出现在响应中
        write_only=True,

        # 允许传入 null，用于取消用户当前角色
        allow_null=True,

        required=True,

        error_messages={
            "required": "必须提交角色ID",
            "does_not_exist": "角色不存在或已被停用",
            "incorrect_type": "角色ID格式错误",
        },
    )

    class Meta:
        model = User
        fields = [
            "role_id",
        ]

    def update(self, instance, validated_data):
        """
        修改用户角色。

        因为 role_id 使用了 source="role"，
        所以 validated_data 中的字段名是 role。
        """

        instance.role = validated_data["role"]

        # 只更新 role 字段
        instance.save(update_fields=["role"])

        return instance