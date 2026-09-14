"""
-*- coding: utf-8 -*-
@File  : login.py
@Author: 61ackPink
@Time : 2026/9/11 15:17
@Desc : 用户登录序列化器
"""

from rest_framework import serializers

from apps.users.models import User


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""

    # 登录时前端需要提交用户名
    username = serializers.CharField(
        max_length=50,
        trim_whitespace=True,
    )
    # write_only=True 表示密码只用于接收请求
    # 序列化响应时不会返回密码
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_username(self, value):
        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "用户名不能包含空格"
            )
        return value

    def validate_password(self, value):
        if any(character.isspace() for character in value):
            raise serializers.ValidationError(
                "密码不能包含空格"
            )
        return value

    def validate(self, attrs):
        """
        检查用户名、密码和账号状态。

        validate() 验证的是多个字段之间的逻辑。
        因为登录需要同时检查 username 和 password，
        所以放在这里最合适。
        """

        username = attrs["username"]
        password = attrs["password"]

        try:
            # 根据用户名查询用户
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 不告诉前端具体是用户名不存在还是密码错误，
            # 避免别人通过接口猜测系统中有哪些账号
            raise serializers.ValidationError(
                "用户名或密码错误"
            )

        # 调用模型中的 check_password()
        # 它会将用户输入的密码与数据库中的哈希密码进行比较
        if not user.check_password(password):
            raise serializers.ValidationError(
                "用户名或密码错误"
            )

        # 即使用户名和密码正确，被禁用的账号也不能登录
        if not user.is_active:
            raise serializers.ValidationError(
                "账号已被禁用"
            )

        # 把查询到的用户对象放进验证结果中
        # 后面的登录视图可以通过 validated_data["user"] 取得它
        attrs["user"] = user

        return attrs

"""
接收用户名和密码
    ↓
查询用户是否存在
    ↓
调用 check_password() 验证密码
    ↓
检查账号是否启用
    ↓
把 user 对象交给登录视图
"""
