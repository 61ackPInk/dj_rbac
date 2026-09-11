from pathlib import Path

# 根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# KEY
SECRET_KEY = 'django-insecure-l%cev$0umo&8kpcbc&utg9zb30p3teb38wqt&f+b1k0331+f+^'

DEBUG = True
ALLOWED_HOSTS = []

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
DATABASES = {
    'default': {
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        'NAME': 'dj_rbac',
        'USER': 'root',
        'PASSWORD': '010601',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'POOL_OPTIONS': {
            'POOL_SIZE': 10,
            'MAX_OVERFLOW': 10,
            'RECYCLE': 24 * 60 * 60,
            'TIMEOUT': 30,
        }
    }
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