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
    )
]

