from django.urls import path, include

urlpatterns = [
    # 示例API
    path(
        'example/',
        include('apps.example.urls')
    ),
    # 用户模块API
    path(
        'api/',
        include('apps.users.urls')
    ),
    # 页面管理模块API
    path(
        "api/pages/",
        include("apps.pages.urls"),
    ),
    # 仪表盘【数据概览】
    path(
        "api/dashboards/",
        include("apps.dashboards.urls"),
    ),
]
