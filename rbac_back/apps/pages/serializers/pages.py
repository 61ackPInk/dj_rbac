"""
-*- coding: utf-8 -*-
@File  : pages.py
@Author: 61ackPink
@Time : 2026/9/16 15:14
@Desc : 页面序列化器
"""
from rest_framework import serializers

from apps.pages.models import Page
from apps.users.models import Role

class PageParentInfoSerializer(
    serializers.ModelSerializer
):
    """父页面简要信息"""

    class Meta:
        model = Page

        fields = [
            "id",
            "name",
            "code",
            "path",
        ]

        read_only_fields = fields


class PageRoleInfoSerializer(
    serializers.ModelSerializer
):
    """页面可见角色简要信息"""

    class Meta:
        model = Role

        fields = [
            "id",
            "name",
            "code",
            "rank",
        ]

        read_only_fields = fields


class PageSerializer(serializers.ModelSerializer):
    """页面创建、修改和查询序列化器"""

    # 用于响应，返回父页面的详细信息
    parent = PageParentInfoSerializer(
        read_only=True,
    )

    # 用于请求，接收父页面 ID
    #
    # source="parent" 表示验证成功后，
    # validated_data 中使用 parent 作为字段名。
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Page.objects.all(),
        source="parent",
        write_only=True,
        required=False,
        allow_null=True,
        error_messages={
            "does_not_exist": "父页面不存在",
            "incorrect_type": "父页面ID格式错误",
        },
    )

    # 用于响应，返回页面已分配的角色信息
    visible_roles = PageRoleInfoSerializer(
        many=True,
        read_only=True,
    )

    # 用于请求，接收角色 ID 数组
    visible_role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.filter(is_active=True),
        source="visible_roles",
        many=True,
        write_only=True,
        required=False,
        error_messages={
            "does_not_exist": "角色不存在或已被停用",
            "incorrect_type": "角色ID格式错误",
        },
    )

    code = serializers.RegexField(
        # 页面编码必须以字母开头，
        # 后续只能使用字母、数字和下划线
        regex=r"^[A-Za-z][A-Za-z0-9_]*$",
        min_length=1,
        max_length=100,
        trim_whitespace=True,
        error_messages={
            "blank": "页面编码不能为空",
            "invalid": "页面编码必须以字母开头，且只能包含字母、数字和下划线",
            "max_length": "页面编码不能超过100个字符",
        },
    )

    path = serializers.CharField(
        max_length=255,
        trim_whitespace=False,
        error_messages={
            "blank": "页面路由不能为空",
            "max_length": "页面路由不能超过255个字符",
        },
    )

    class Meta:
        model = Page

        fields = [
            "id",
            "name",
            "code",
            "path",
            "component",
            "icon",
            "parent",
            "parent_id",
            "visible_roles",
            "visible_role_ids",
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

    def validate_code(self, value):
        """统一将页面编码转换为大写"""

        return value.upper()

    def validate_path(self, value):
        """验证前端页面路由"""

        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "页面路由不能包含空格"
            )

        if not value.startswith("/"):
            raise serializers.ValidationError(
                "页面路由必须以 / 开头"
            )

        return value

    def validate(self, attrs):
        """
        验证页面唯一性以及父子页面关系。
        """

        current_page = self.instance

        code = attrs.get("code")
        path = attrs.get("path")

        # --------------------
        # 页面编码唯一性
        # --------------------

        if code:
            code_queryset = Page.objects.filter(
                code=code
            )

            if current_page:
                code_queryset = code_queryset.exclude(
                    id=current_page.id
                )

            if code_queryset.exists():
                raise serializers.ValidationError({
                    "code": "页面编码已经存在"
                })

        # --------------------
        # 页面路由唯一性
        # --------------------

        if path:
            path_queryset = Page.objects.filter(
                path=path
            )

            if current_page:
                path_queryset = path_queryset.exclude(
                    id=current_page.id
                )

            if path_queryset.exists():
                raise serializers.ValidationError({
                    "path": "页面路由已经存在"
                })

        # PATCH 请求没有提交 parent_id 时，
        # attrs 中不会出现 parent，所以不需要重新验证。
        if "parent" not in attrs:
            return attrs

        parent = attrs["parent"]

        # parent=null 表示设置成顶级页面
        if parent is None:
            return attrs

        # 创建页面时还没有当前页面 ID，
        # 不可能把自己设置为父页面。
        if current_page is None:
            return attrs

        # 页面不能直接成为自己的父页面
        if parent.id == current_page.id:
            raise serializers.ValidationError({
                "parent_id": "页面不能将自己设置为父页面"
            })

        # 防止形成循环关系。
        #
        # 例如原来：
        # A → B → C
        #
        # 不允许把 A 的父页面设置成 C，
        # 否则会形成 A → B → C → A。
        ancestor = parent

        while ancestor is not None:
            if ancestor.id == current_page.id:
                raise serializers.ValidationError({
                    "parent_id": "父页面不能是当前页面的子页面"
                })

            ancestor = ancestor.parent

        return attrs


class VisiblePageSerializer(serializers.ModelSerializer):
    """普通用户可见页面信息"""

    class Meta:
        model = Page

        # 只返回前端导航需要的信息，
        # 不暴露页面分配给了哪些角色
        fields = [
            "id",
            "name",
            "code",
            "path",
            "component",
            "icon",
            "parent_id",
            "sort_order",
        ]

        read_only_fields = fields

