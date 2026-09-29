"""
-*- coding: utf-8 -*-
@File  : role_permissions.py
@Author: 61ackPink
@Time : 2026/9/28 17:16
@Desc : 角色操作权限分配序列化器
"""

from rest_framework import serializers

from apps.users.models import Permission, Role


class RolePermissionAssignSerializer(
    serializers.ModelSerializer
):
    """给角色分配操作权限"""

    permission_ids = serializers.PrimaryKeyRelatedField(
        # 只能分配处于启用状态，
        # 并且所属页面也处于启用状态的权限
        queryset=Permission.objects.filter(
            is_active=True,
            page__is_active=True,
        ),
        source="permissions",
        many=True,
        write_only=True,
        error_messages={
            "required": "请提交权限ID列表",
            "does_not_exist": (
                "权限不存在、已停用，"
                "或所属页面已停用"
            ),
            "incorrect_type": "权限ID格式错误",
            "not_a_list": "权限ID必须使用数组格式",
        },
    )

    class Meta:
        model = Role

        fields = [
            "permission_ids",
        ]

    def validate_permission_ids(self, value):
        """
        防止提交重复的权限 ID。

        PrimaryKeyRelatedField 验证完成后，
        value 中保存的是 Permission 对象列表。
        """

        permission_ids = [
            permission.id
            for permission in value
        ]

        if len(permission_ids) != len(
            set(permission_ids)
        ):
            raise serializers.ValidationError(
                "权限ID不能重复"
            )

        return value

    def validate(self, attrs):
        """
        检查角色是否拥有权限对应的页面。

        页面权限和操作权限是两层控制：

        1. 角色必须拥有页面；
        2. 角色还必须拥有页面中的具体操作权限。
        """

        role = self.instance

        permissions = attrs.get(
            "permissions",
            [],
        )

        # 根管理员身份不依赖角色，
        # 普通角色的操作权限必须属于该角色可见页面
        visible_page_ids = set(
            role.pages.values_list(
                "id",
                flat=True,
            )
        )

        invalid_permissions = [
            permission
            for permission in permissions
            if permission.page_id
            not in visible_page_ids
        ]

        if invalid_permissions:
            invalid_codes = [
                permission.code
                for permission
                in invalid_permissions
            ]

            raise serializers.ValidationError({
                "permission_ids": (
                    "角色尚未拥有以下权限所属的页面："
                    + "、".join(invalid_codes)
                ),
            })

        return attrs

    def update(self, instance, validated_data):
        """替换角色当前拥有的操作权限"""

        permissions = validated_data[
            "permissions"
        ]

        # set() 会让角色的权限列表
        # 与本次提交的数据完全一致
        instance.permissions.set(
            permissions,
        )

        return instance