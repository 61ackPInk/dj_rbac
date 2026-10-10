from django.apps import AppConfig


class DashboardsConfig(AppConfig):
    # 与项目现有 app 保持一致
    default_auto_field = "django.db.models.BigAutoField"

    # 因为 dashboards 位于 apps 目录下，这里要写完整导入路径
    name = "apps.dashboards"

    # Django 后台展示的应用名称
    verbose_name = "仪表盘"