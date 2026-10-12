"""
-*- coding: utf-8 -*-
@File  : 0006_permission_role_permissions_and_more.py
@Author: 61ackPink
@Time : 2026/10/12 11:37
@Desc : 创建操作权限及角色操作权限关系
"""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    """创建 RBAC 操作权限相关数据表。"""

    # ====================
    # 迁移依赖
    # ====================

    dependencies = [
        (
            "pages",
            "0001_initial",
        ),
        (
            "users",
            "0005_user_token_version",
        ),
    ]

    # ====================
    # 迁移操作
    # ====================

    operations = [
        # 创建操作权限表
        migrations.CreateModel(
            name="Permission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=50,
                        verbose_name="权限名称",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        db_index=True,
                        max_length=100,
                        unique=True,
                        verbose_name="权限编码",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        default="",
                        max_length=255,
                        verbose_name="权限描述",
                    ),
                ),
                (
                    "sort_order",
                    models.PositiveIntegerField(
                        db_index=True,
                        default=0,
                        verbose_name="排序",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        verbose_name="是否启用",
                    ),
                ),
                (
                    "create_time",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="创建时间",
                    ),
                ),
                (
                    "update_time",
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name="更新时间",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=(
                            django.db.models
                            .deletion.PROTECT
                        ),
                        related_name="permissions",
                        to="pages.page",
                        verbose_name="所属页面",
                    ),
                ),
            ],
            options={
                "verbose_name": "操作权限",
                "verbose_name_plural": "操作权限",
                "db_table": "sys_permissions",
                "ordering": [
                    "page_id",
                    "sort_order",
                    "id",
                ],
            },
        ),

        # 创建角色与操作权限的多对多关系
        migrations.AddField(
            model_name="role",
            name="permissions",
            field=models.ManyToManyField(
                blank=True,
                db_table="sys_role_permissions",
                related_name="roles",
                to="users.permission",
                verbose_name="操作权限",
            ),
        ),

        # 同一个页面中不允许出现同名权限
        migrations.AddConstraint(
            model_name="permission",
            constraint=models.UniqueConstraint(
                fields=(
                    "page",
                    "name",
                ),
                name=(
                    "unique_permission_name_per_page"
                ),
            ),
        ),
    ]