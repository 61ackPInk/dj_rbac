"""
-*- coding: utf-8 -*-
@File  : permissions.py
@Author: 61ackPink
@Time : 2026/9/28 16:51
@Desc : 操作权限模型
"""

from django.db import models


class Permission(models.Model):
    """
    操作权限。

    每条权限代表某个页面中的一个具体操作，例如：

    USER_LIST       查看用户列表
    USER_CREATE     创建用户
    USER_UPDATE     修改用户
    USER_DISABLE    停用用户
    """

    name = models.CharField(
        max_length=50,
        verbose_name="权限名称",
    )

    code = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name="权限编码",
    )

    page = models.ForeignKey(
        "pages.Page",

        # 页面仍然被权限使用时，不允许物理删除
        on_delete=models.PROTECT,

        # 可以通过 page.permissions.all()
        # 查询该页面下的全部操作权限
        related_name="permissions",

        verbose_name="所属页面",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="权限描述",
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
        db_table = "sys_permissions"
        verbose_name = "操作权限"
        verbose_name_plural = verbose_name

        # 先按页面排序，同一页面内再按 sort_order 排序
        ordering = [
            "page_id",
            "sort_order",
            "id",
        ]

        constraints = [
            # 同一个页面中不能出现两个同名权限
            models.UniqueConstraint(
                fields=[
                    "page",
                    "name",
                ],
                name="unique_permission_name_per_page",
            ),
        ]

    def __str__(self):
        return f"{self.name}（{self.code}）"