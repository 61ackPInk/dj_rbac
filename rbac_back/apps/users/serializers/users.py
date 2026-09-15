"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/11 16:20
@Desc : 用户信息和状态
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


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    """根管理员修改用户基本信息"""

    username = serializers.CharField(
        required=False,
        min_length=4,
        max_length=20,
        trim_whitespace=False,
        error_messages={
            "blank": "用户名不能为空",
            "min_length": "用户名不能少于4个字符",
            "max_length": "用户名不能超过20个字符",
        },
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            "invalid": "邮箱格式不正确",
        },
    )

    is_active = serializers.BooleanField(
        required=False,
        error_messages={
            "invalid": "用户状态必须是布尔值",
        },
    )

    class Meta:
        model = User

        # 只允许管理员修改以下三个字段
        fields = [
            "username",
            "email",
            "is_active",
        ]

    def validate_username(self, value):
        """验证用户名"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "用户名不能包含空格"
            )

        # 修改用户时，排除当前用户自身。
        # 否则保留原用户名也会被判断为重复。
        queryset = User.objects.filter(
            username=value
        )

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "用户名已经存在"
            )

        return value

    def validate_email(self, value):
        """
        统一空邮箱的保存形式。

        前端传入空字符串时，将其转换为 None，
        数据库最终保存为 NULL。
        """

        if value == "":
            return None

        return value

    def validate(self, attrs):
        """执行涉及当前用户对象的验证"""

        user = self.instance
        is_active = attrs.get("is_active")

        # 不允许通过普通用户管理接口禁用根管理员
        if (
            user
            and user.is_root
            and is_active is False
        ):
            raise serializers.ValidationError({
                "is_active": "不能禁用根管理员账号"
            })

        return attrs


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """当前用户修改自己的基本资料"""

    username = serializers.CharField(
        required=False,
        min_length=4,
        max_length=20,
        trim_whitespace=False,
        error_messages={
            "blank": "用户名不能为空",
            "min_length": "用户名不能少于4个字符",
            "max_length": "用户名不能超过20个字符",
        },
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            "invalid": "邮箱格式不正确",
        },
    )

    class Meta:
        model = User

        # 普通用户只能修改用户名和邮箱
        fields = [
            "username",
            "email",
        ]

    def validate_username(self, value):
        """验证用户名"""

        # 用户名中不能出现空格、制表符或换行符
        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "用户名不能包含空格"
            )

        # 检查用户名是否已经被其他用户使用
        queryset = User.objects.filter(
            username=value
        )

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "用户名已经存在"
            )

        return value

    def validate_email(self, value):
        """统一空邮箱的保存形式"""

        if value == "":
            return None

        return value