"""
-*- coding: utf-8 -*-
@File  : roles.py
@Author: 61ackPink
@Time : 2026/9/14 16:57
@Desc : 角色序列化器
"""
from rest_framework import serializers

from apps.users.models import Role

class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""

    name = serializers.CharField(
        min_length=2,
        max_length=50,
        trim_whitespace=True,
        error_messages={
            "blank": "角色名称不能为空",
            "min_length": "角色名称不能少于2个字符",
            "max_length": "角色名称不能超过50个字符",
        },
    )
    code = serializers.RegexField(
        # 编码必须以字母开头，
        # 后面只能使用字母、数字和下划线
        regex=r"^[A-Za-z][A-Za-z0-9_]*$",
        min_length=1,
        max_length=50,
        trim_whitespace=True,
        error_messages={
            "blank": "角色编码不能为空",
            "invalid": "角色编码必须以字母开头，且只能包含字母、数字和下划线",
            "max_length": "角色编码不能超过50个字符",
        },
    )
    rank = serializers.IntegerField(
        min_value=1,
        error_messages={
            "required": "角色权重不能为空",
            "invalid": "角色权重必须是整数",
            "min_value": "角色权重必须大于0",
        },
    )

    class Meta:
        model = Role

        fields = [
            "id",
            "name",
            "code",
            "rank",
            "description",
            "is_active",
            "create_time",
            "update_time",
        ]

        # 这些字段由数据库自动生成，前端不能修改
        read_only_fields = [
            "id",
            "create_time",
            "update_time",
        ]

        # 暂时关闭 ModelSerializer 自动生成的唯一性验证，
        # 由下面的 validate() 统一处理创建和修改场景
        extra_kwargs = {
            "name": {
                "validators": [],
            },
            "code": {
                "validators": [],
            },
        }

    def validate_code(self, value):
        """
        统一将角色编码转换成大写。

        例如：
            admin        → ADMIN
            finance_admin → FINANCE_ADMIN
        """

        return value.upper()

    def validate(self, attrs):
        """检查角色名称和编码是否重复"""

        # 修改角色时，self.instance 是当前角色对象；
        # 创建角色时，self.instance 为 None。
        current_role = self.instance

        name = attrs.get("name")
        code = attrs.get("code")

        if name:
            name_queryset = Role.objects.filter(name=name)

            # 修改角色时排除当前记录，
            # 否则原来的名称会被误判为重复
            if current_role:
                name_queryset = name_queryset.exclude(
                    id=current_role.id
                )

            if name_queryset.exists():
                raise serializers.ValidationError({
                    "name": "角色名称已经存在"
                })

        if code:
            code_queryset = Role.objects.filter(code=code)

            if current_role:
                code_queryset = code_queryset.exclude(
                    id=current_role.id
                )

            if code_queryset.exists():
                raise serializers.ValidationError({
                    "code": "角色编码已经存在"
                })

        return attrs
