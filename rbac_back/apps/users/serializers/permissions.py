"""
-*- coding: utf-8 -*-
@File  : permissions.py
@Author: 61ackPink
@Time : 2026/9/28 16:55
@Desc : 操作权限序列化器
"""

from rest_framework import serializers

from apps.pages.models import Page
from apps.users.models import Permission


class PermissionPageInfoSerializer(
    serializers.ModelSerializer
):
    """权限所属页面的简要信息"""

    class Meta:
        model = Page

        fields = [
            "id",
            "name",
            "code",
            "path",
        ]

        read_only_fields = fields


class PermissionSerializer(
    serializers.ModelSerializer
):
    """操作权限创建、修改和查询序列化器"""

    # 响应时返回页面的基本信息
    page = PermissionPageInfoSerializer(
        read_only=True,
    )

    # 请求时通过 page_id 指定所属页面
    page_id = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.filter(
            is_active=True,
        ),
        source="page",
        write_only=True,
        error_messages={
            "required": "所属页面不能为空",
            "does_not_exist": "页面不存在或已被停用",
            "incorrect_type": "页面ID格式错误",
        },
    )

    code = serializers.RegexField(
        # 权限编码必须以字母开头，
        # 后面只能包含字母、数字和下划线
        regex=r"^[A-Za-z][A-Za-z0-9_]*$",
        min_length=1,
        max_length=100,
        trim_whitespace=True,
        error_messages={
            "blank": "权限编码不能为空",
            "invalid": (
                "权限编码必须以字母开头，"
                "且只能包含字母、数字和下划线"
            ),
            "max_length": "权限编码不能超过100个字符",
        },
    )

    name = serializers.CharField(
        min_length=2,
        max_length=50,
        trim_whitespace=True,
        error_messages={
            "blank": "权限名称不能为空",
            "min_length": "权限名称不能少于2个字符",
            "max_length": "权限名称不能超过50个字符",
        },
    )

    class Meta:
        model = Permission

        fields = [
            "id",
            "name",
            "code",
            "page",
            "page_id",
            "description",
            "sort_order",
            "is_active",
            "create_time",
            "update_time",
        ]

        read_only_fields = [
            "id",
            "create_time",
            "update_time",
        ]

        # 关闭 ModelSerializer 自动生成的唯一性验证，
        # 统一在 validate() 中返回中文提示
        extra_kwargs = {
            "code": {
                "validators": [],
            },
        }

    def validate_code(self, value):
        """
        权限编码统一保存为大写。

        例如：
        user_list → USER_LIST
        """

        return value.upper()

    def validate(self, attrs):
        """检查权限编码以及页面内名称是否重复"""

        current_permission = self.instance

        code = attrs.get("code")
        name = attrs.get("name")

        # PATCH 没有提交 page_id 时，
        # 使用当前权限原来的所属页面
        page = attrs.get(
            "page",
            getattr(
                current_permission,
                "page",
                None,
            ),
        )

        # --------------------
        # 权限编码唯一性
        # --------------------

        if code:
            code_queryset = Permission.objects.filter(
                code=code,
            )

            if current_permission:
                code_queryset = code_queryset.exclude(
                    id=current_permission.id,
                )

            if code_queryset.exists():
                raise serializers.ValidationError({
                    "code": "权限编码已经存在",
                })

        # --------------------
        # 同一页面内权限名称唯一
        # --------------------

        if name and page:
            name_queryset = Permission.objects.filter(
                page=page,
                name=name,
            )

            if current_permission:
                name_queryset = name_queryset.exclude(
                    id=current_permission.id,
                )

            if name_queryset.exists():
                raise serializers.ValidationError({
                    "name": (
                        "当前页面中已经存在"
                        "相同名称的权限"
                    ),
                })

        return attrs