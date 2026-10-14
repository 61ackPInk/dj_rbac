"""
-*- coding: utf-8 -*-
@File  : settings.py
@Author: 61ackPink
@Time : 2026/10/13
@Desc : Django 项目配置
"""

import os
from pathlib import Path

from django.core.exceptions import (
    ImproperlyConfigured,
)
from dotenv import load_dotenv


# ==================== 项目路径与环境文件 ====================

BASE_DIR = Path(
    __file__
).resolve().parent.parent

BACKEND_ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=BACKEND_ENV_FILE,
    override=False,
)

# ==================== 环境变量读取工具 ====================

def get_required_environment(
    name,
):
    """读取必须配置的环境变量。"""

    value = os.getenv(
        name,
        "",
    ).strip()

    if not value:
        raise ImproperlyConfigured(
            f"缺少环境变量：{name}"
        )

    return value


def get_boolean_environment(
    name,
    default=False,
):
    """读取布尔类型环境变量。"""

    value = os.getenv(name)

    if value is None:
        return default

    normalized_value = (
        value.strip().lower()
    )

    if normalized_value in {
        "true",
        "1",
        "yes",
        "on",
    }:
        return True

    if normalized_value in {
        "false",
        "0",
        "no",
        "off",
    }:
        return False

    raise ImproperlyConfigured(
        f"环境变量 {name} 必须是布尔值"
    )


def get_integer_environment(
    name,
    default,
):
    """读取整数类型环境变量。"""

    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    try:
        return int(raw_value)
    except ValueError as error:
        raise ImproperlyConfigured(
            f"环境变量 {name} 必须是整数"
        ) from error


def get_list_environment(
    name,
    default="",
):
    """读取英文逗号分隔的列表环境变量。"""

    raw_value = os.getenv(
        name,
        default,
    )

    return [
        item.strip()
        for item in raw_value.split(",")
        if item.strip()
    ]


# ==================== Django 基础配置 ====================

SECRET_KEY = get_required_environment(
    "DJANGO_SECRET_KEY"
)

DEBUG = get_boolean_environment(
    "DJANGO_DEBUG",
    default=False,
)

ALLOWED_HOSTS = get_list_environment(
    "DJANGO_ALLOWED_HOSTS"
)

CSRF_TRUSTED_ORIGINS = (
    get_list_environment(
        "DJANGO_CSRF_TRUSTED_ORIGINS"
    )
)

# APP
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 安装应用
    'rest_framework',

    # 自己创建的应用
    'apps.example',
    'apps.users',
    'apps.pages',
    'apps.dashboards',
    'apps.products',
    'apps.data_collectors',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rbac_back.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rbac_back.wsgi.application'

# Database
# ==================== MySQL 数据库配置 ====================

DATABASES = {
    "default": {
        "ENGINE": (
            "dj_db_conn_pool.backends.mysql"
        ),
        "NAME": get_required_environment(
            "DB_NAME"
        ),
        "USER": get_required_environment(
            "DB_USER"
        ),
        "PASSWORD": get_required_environment(
            "DB_PASSWORD"
        ),
        "HOST": os.getenv(
            "DB_HOST",
            "127.0.0.1",
        ),
        "PORT": get_integer_environment(
            "DB_PORT",
            3306,
        ),
        "POOL_OPTIONS": {
            "POOL_SIZE": (
                get_integer_environment(
                    "DB_POOL_SIZE",
                    10,
                )
            ),
            "MAX_OVERFLOW": (
                get_integer_environment(
                    "DB_MAX_OVERFLOW",
                    10,
                )
            ),
            "RECYCLE": (
                get_integer_environment(
                    "DB_RECYCLE_SECONDS",
                    86400,
                )
            ),
            "TIMEOUT": (
                get_integer_environment(
                    "DB_TIMEOUT_SECONDS",
                    30,
                )
            ),
        },
    },
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF 配置
REST_FRAMEWORK = {
    # 所有 JSON 响应都使用自定义 Renderer
    "DEFAULT_RENDERER_CLASSES": (
        "common.custom.json_render.Renderer",
    ),
    # 所有接口默认使用自定义 JWT 身份认证
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "common.authentication.jwt_authentication.JWTAuthentication",
    ),
    # 所有接口默认要求用户已经登录
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

# JWT 配置
JWT_AUTH = {
    # JWT 使用的签名算法
    "ALGORITHM": "HS256",

    # access_token 有效时间：30 分钟
    "ACCESS_TOKEN_LIFETIME_MINUTES": 30,

    # refresh_token 有效时间：7 天
    "REFRESH_TOKEN_LIFETIME_DAYS": 7,
}
