"""
-*- coding: utf-8 -*-
@File  : passwords.py
@Author: 61ackPink
@Time : 2026/9/15 17:31
@Desc : 密码
"""
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from rest_framework import serializers


class UserPasswordChangeSerializer(
    serializers.Serializer
):
    """当前用户修改自己的密码"""

    old_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    new_password = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    def validate_old_password(self, value):
        """验证原密码"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "原密码不能包含空格"
            )

        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "原密码错误"
            )

        return value

    def validate_new_password(self, value):
        """检查新密码中的空白字符"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "新密码不能包含空格"
            )

        return value

    def validate_new_password_confirm(self, value):
        """检查确认密码中的空白字符"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "确认密码不能包含空格"
            )

        return value

    def validate(self, attrs):
        """验证两次新密码及密码强度"""

        user = self.context["request"].user
        new_password = attrs["new_password"]
        new_password_confirm = attrs[
            "new_password_confirm"
        ]

        if new_password != new_password_confirm:
            raise serializers.ValidationError({
                "new_password_confirm": "两次输入的新密码不一致"
            })

        # 新密码不能和原密码相同
        if user.check_password(new_password):
            raise serializers.ValidationError({
                "new_password": "新密码不能与原密码相同"
            })

        try:
            # 将当前用户传给 Django，
            # 可以同时检查密码是否与用户名过于相似
            django_validate_password(
                new_password,
                user=user,
            )
        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "new_password": list(error.messages)
            })

        return attrs

    def create(self, validated_data):
        """
        修改当前用户密码。

        普通 Serializer 没有默认的 create()，
        所以需要自行实现。
        """

        user = self.context["request"].user

        # 使用哈希方式保存新密码
        user.set_password(
            validated_data["new_password"]
        )

        # 递增 Token 版本，使旧 Token 全部失效
        user.token_version += 1

        user.save(
            update_fields=[
                "password",
                "token_version",
            ]
        )

        return user


class UserPasswordResetSerializer(serializers.Serializer):
    """根管理员重置普通用户密码"""

    new_password = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    new_password_confirm = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    def validate_new_password(self, value):
        """检查新密码中的空白字符"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "新密码不能包含空格"
            )

        return value

    def validate_new_password_confirm(self, value):
        """检查确认密码中的空白字符"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "确认密码不能包含空格"
            )

        return value

    def validate(self, attrs):
        """验证管理员提交的新密码"""

        user = self.instance
        new_password = attrs["new_password"]

        # 根管理员密码不能通过用户管理接口重置，
        # 根管理员应通过自己的修改密码接口操作
        if user.is_root:
            raise serializers.ValidationError(
                "不能通过用户管理接口重置根管理员密码"
            )

        if (
            new_password
            != attrs["new_password_confirm"]
        ):
            raise serializers.ValidationError({
                "new_password_confirm": "两次输入的新密码不一致"
            })

        if user.check_password(new_password):
            raise serializers.ValidationError({
                "new_password": "新密码不能与原密码相同"
            })

        try:
            django_validate_password(
                new_password,
                user=user,
            )
        except DjangoValidationError as error:
            raise serializers.ValidationError({
                "new_password": list(error.messages)
            })

        return attrs

    def update(self, instance, validated_data):
        """重置指定用户密码"""

        instance.set_password(
            validated_data["new_password"]
        )

        # 使该用户之前的 access_token 和
        # refresh_token 全部立即失效
        instance.token_version += 1

        instance.save(
            update_fields=[
                "password",
                "token_version",
            ]
        )

        return instance