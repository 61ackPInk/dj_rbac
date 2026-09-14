"""
-*- coding: utf-8 -*-
@File  : roles.py
@Author: 61ackPink
@Time : 2026/9/11 17:38
@Desc : 角色模型
"""
from django.db import models

class Role(models.Model):
    """
    系统角色

    角色名称、编码、权重、
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='角色名称')
    code = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='角色编码')
    rank = models.PositiveIntegerField(default=0, db_index=True, verbose_name='角色权重', help_text='数字越大，等级越高')
    description = models.CharField(max_length=255, blank=True, default='', verbose_name='角色描述')
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
    )

    class Meta:
        db_table = 'sys_roles'
        verbose_name = '系统角色'
        verbose_name_plural = verbose_name

        # 查询角色时，默认按照权重从高到低排序
        # 权重相同时再按照 ID 从小到大排序
        ordering = ["-rank", "id"]

    def __str__(self):
        return f"{self.name}（{self.code}，权重：{self.rank}）"