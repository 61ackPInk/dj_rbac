"""
-*- coding: utf-8 -*-
@File  : jwt_authentication.py
@Author: 61ackPink
@Time : 2026/9/11 16:08
@Desc : JWT 身份认证类
"""
import jwt
from django.conf import settings
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User


class JWTAuthentication(BaseAuthentication):
    """自定义 JWT 身份认证"""
    # 前端请求头需要使用：
    # Authorization: Bearer access_token
    keyword = "Bearer"

    def authenticate(self, request):
        """
        验证请求携带的 JWT。

        验证成功后返回：
            (user, token)

        DRF 会自动设置：
            request.user = user
            request.auth = token
        """
        # 获取 Authorization 请求头，并按空格拆分
        # 例如：
        # ["Bearer", "eyJhbGciOiJIUzI1Ni..."]
        authorization = get_authorization_header(request).split()

        # 没有携带 Authorization 时不进行认证
        # 是否允许匿名访问，由 permission_classes 决定
        if not authorization:
            return None

        # 如果不是 Bearer 类型，就不使用当前认证类处理
        if authorization[0].lower() != self.keyword.lower().encode():
            return None

        # 正确格式必须只有两部分：
        # Bearer + Token
        if len(authorization) != 2:
            raise AuthenticationFailed(
                "Authorization 请求头格式错误"
            )

        try:
            # 请求头读取到的是 bytes，需要转换为字符串
            token = authorization[1].decode("utf-8")
        except UnicodeDecodeError:
            raise AuthenticationFailed("登录凭证格式错误")

        try:
            # 验证 Token 签名并解析载荷
            # PyJWT 会自动检查 exp 过期时间
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[
                    settings.JWT_AUTH["ALGORITHM"]
                ],
            )
        except jwt.ExpiredSignatureError:
            # Token 已超过 exp 时间
            raise AuthenticationFailed("登录凭证已过期")
        except jwt.InvalidTokenError:
            # 签名错误、内容损坏等情况都会进入这里
            raise AuthenticationFailed("无效的登录凭证")

        # 普通接口只能使用 access_token
        # 防止用户拿 refresh_token 直接访问业务接口
        if payload.get("token_type") != "access":
            raise AuthenticationFailed("登录凭证类型错误")

        # 从 Token 中取得用户 ID
        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationFailed(
                "登录凭证缺少用户信息"
            )

        try:
            # 查询用户，同时确保账号处于启用状态
            user = User.objects.get(
                id=user_id,
                is_active=True,
            )
        except User.DoesNotExist:
            raise AuthenticationFailed(
                "用户不存在或已被禁用"
            )

        # 检查 Token 版本
        token_version = payload.get("token_version")

        if token_version != user.token_version:
            raise AuthenticationFailed(
                "登录凭证已失效，请重新登录"
            )

        # 第一个值会成为 request.user
        # 第二个值会成为 request.auth
        return user, token

    def authenticate_header(self, request):
        """
        告诉 DRF 当前认证方式是 Bearer。

        存在这个方法时，未登录通常返回 401；
        如果没有，DRF 可能返回 403。
        """
        return self.keyword