"""
-*- coding: utf-8 -*-
@File  : register.py
@Author: 61ackPink
@Time : 2026/9/11 14:30
@Desc : 用户注册序列化器
"""
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.users.models import Users


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        validators=[validate_password],
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = Users
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
        ]

    def validate_username(self, value):
        """检查用户名"""

        username = value.strip()

        if Users.objects.filter(username=username).exists():
            raise serializers.ValidationError("用户名已经存在")

        return username

    def validate(self, attrs):
        """检查两次密码是否一致"""

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({
                "password_confirm": "两次输入的密码不一致"
            })

        return attrs

    def create(self, validated_data):
        """创建用户"""

        validated_data.pop("password_confirm")
        raw_password = validated_data.pop("password")

        user = Users(**validated_data)
        user.set_password(raw_password)
        user.save()

        return user

"""
前端提交 JSON
    ↓
UserRegisterAPIView.post()
    ↓
UserRegisterSerializer 验证数据
    ↓
检查用户名是否重复
    ↓
检查两次密码是否一致
    ↓
使用 set_password() 加密密码
    ↓
保存到 sys_users
    ↓
返回用户 ID、用户名和邮箱
"""