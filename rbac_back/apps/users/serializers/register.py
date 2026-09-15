"""
-*- coding: utf-8 -*-
@File  : register.py
@Author: 61ackPink
@Time : 2026/9/11 14:30
@Desc : 注册
"""
from django.contrib.auth.password_validation import (
    validate_password as django_validate_password,
)
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from apps.users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        trim_whitespace=False,
        error_messages={
            "blank": "用户名不能为空",
            "min_length": "用户名不能少于4个字符",
            "max_length": "用户名不能超过20个字符",
        },
    )

    password = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    password_confirm = serializers.CharField(
        write_only=True,
        max_length=128,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
        ]

    def validate_username(self, value):
        """验证用户名"""

        # isspace() 不仅能检查普通空格，
        # 还可以检查制表符、换行符等空白字符
        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "用户名不能包含空格"
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "用户名已经存在"
            )

        return value

    def validate_password(self, value):
        """验证密码"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "密码不能包含空格"
            )

        try:
            # 使用 settings.py 中配置的 Django 密码验证规则
            django_validate_password(value)
        except DjangoValidationError as error:
            # 把 Django 的错误转换为 DRF 能返回的错误
            raise serializers.ValidationError(
                list(error.messages)
            )

        return value

    def validate_password_confirm(self, value):
        """验证确认密码中的空格"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "确认密码不能包含空格"
            )

        return value

    def validate(self, attrs):
        """检查两次密码是否一致"""

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "两次输入的密码不一致"
            })

        return attrs

    def create(self, validated_data):
        """创建用户并加密密码"""

        validated_data.pop("password_confirm")
        raw_password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(raw_password)
        user.save()

        return user


# 前端提交 JSON
#     ↓
# UserRegisterAPIView.post()
#     ↓
# UserRegisterSerializer 验证数据
#     ↓
# 检查用户名是否重复
#     ↓
# 检查两次密码是否一致
#     ↓
# 使用 set_password() 加密密码
#     ↓
# 保存到 sys_users
#     ↓
# 返回用户 ID、用户名和邮箱
