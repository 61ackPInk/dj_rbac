"""
-*- coding: utf-8 -*-
@File  : example.py
@Author: 61ackPink
@Time : 2026/9/10 14:57
@Desc : 示例：模型
"""
from django.db import models

class Example(models.Model):
    """示例模型"""
    name = models.CharField(max_length=20, verbose_name='姓名')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    is_active = models.BooleanField(default=True, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'example'
        verbose_name = '示例'

    def __str__(self):
        return self.name