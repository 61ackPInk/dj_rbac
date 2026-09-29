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


class CurrentUserInfoSerializer(UserInfoSerializer):
    """
    当前登录用户信息序列化器。

    在普通用户信息基础上，
    额外返回当前用户拥有的操作权限编码。

    该序列化器只用于 /api/auth/me/，
    不用于管理员查询用户列表，
    避免查询每个用户时重复读取权限。
    """

    permission_codes = serializers.SerializerMethodField(
        method_name="get_permission_codes",
    )

    class Meta(UserInfoSerializer.Meta):
        fields = [
            *UserInfoSerializer.Meta.fields,
            "permission_codes",
        ]

        read_only_fields = fields

    def get_permission_codes(self, user):
        """返回当前用户有效的操作权限编码"""

        # 根管理员不依赖角色操作权限。
        #
        # 前端通过 is_root 判断根管理员，
        # 因此这里不需要查询并返回全部权限。
        if user.is_root:
            return []

        # 普通用户没有角色时没有任何操作权限
        if user.role_id is None:
            return []

        role = user.role

        # 角色停用后不能继续使用该角色权限
        if not role.is_active:
            return []

        permission_codes = (
            role.permissions.filter(
                # 操作权限本身必须启用
                is_active=True,

                # 权限所属页面必须启用
                page__is_active=True,

                # 角色还必须拥有权限所属页面
                page__visible_roles=role,
            )
            .values_list(
                "code",
                flat=True,
            )
            .distinct()
            .order_by(
                "code",
            )
        )

        # QuerySet 不能直接作为最终 JSON 数组，
        # 因此转换为 Python 列表
        return list(permission_codes)


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

    class Meta:
        model = User

        # 只允许管理员修改以下三个字段
        fields = [
            "username",
            "email",
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


class UserStatusUpdateSerializer(serializers.ModelSerializer):
    """管理员修改用户启用状态"""

    is_active = serializers.BooleanField(
        required=True,
        error_messages={
            "required": "必须提交用户状态",
            "invalid": "用户状态必须是布尔值",
        },
    )

    class Meta:
        model = User

        fields = [
            "is_active",
        ]

    def validate(self, attrs):
        """禁止停用根管理员账号"""

        user = self.instance
        is_active = attrs["is_active"]

        if user.is_root and is_active is False:
            raise serializers.ValidationError({
                "is_active": "不能停用根管理员账号",
            })

        return attrs