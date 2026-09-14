"""
-*- coding: utf-8 -*-
@File  : user_roles.py
@Author: 61ackPink
@Time : 2026/9/14 18:20
@Desc : 用户角色关联模型
"""
from django.db import models


class UserRole(models.Model):
    """用户与角色的关联记录"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="role_assignments",
        verbose_name="用户",
    )

    role = models.ForeignKey(
        "users.Role",
        on_delete=models.CASCADE,
        related_name="user_assignments",
        verbose_name="角色",
    )

    assigned_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_role_records",
        verbose_name="分配人",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="是否有效",
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="分配时间",
    )

    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "sys_user_roles"
        verbose_name = "用户角色关联"
        verbose_name_plural = verbose_name

        constraints = [
            # 同一个用户不能重复关联同一个角色
            models.UniqueConstraint(
                fields=["user", "role"],
                name="unique_user_role",
            ),
        ]

        indexes = [
            # 优化查询用户有效角色的速度
            models.Index(
                fields=["user", "is_active"],
                name="idx_user_role_active",
            ),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
