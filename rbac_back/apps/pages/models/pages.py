"""
-*- coding: utf-8 -*-
@File  : pages.py
@Author: 61ackPink
@Time : 2026/9/16 15:06
@Desc : 页面模型
"""
from django.db import models


class Page(models.Model):
    """系统页面"""

    name = models.CharField(
        max_length=100,
        verbose_name="页面名称",
    )

    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="页面编码",
    )

    path = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="页面路由",
    )

    component = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="前端组件",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="页面图标",
    )

    parent = models.ForeignKey(
        "self",

        # 如果页面还有子页面，不允许直接删除父页面
        on_delete=models.PROTECT,

        blank=True,
        null=True,

        # 可以通过 page.children.all() 查询子页面
        related_name="children",

        verbose_name="父页面",
    )

    visible_roles = models.ManyToManyField(
        "users.Role",

        # 可以通过 role.pages.all() 查询该角色拥有的页面
        related_name="pages",

        blank=True,

        # 明确指定中间表名称
        db_table="sys_page_roles",

        verbose_name="可见角色",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        verbose_name="排序",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="是否启用",
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "sys_pages"
        verbose_name = "系统页面"
        verbose_name_plural = verbose_name

        # 数值越小越靠前
        ordering = [
            "sort_order",
            "id",
        ]

    def __str__(self):
        return f"{self.name}（{self.path}）"