"""
-*- coding: utf-8 -*-
@File  : users.py
@Author: 61ackPink
@Time : 2026/9/10 16:59
@Desc : 用户模型
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    """用户表"""
    username = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='用户名')
    password = models.CharField(max_length=128, verbose_name='密码')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    is_root = models.BooleanField(default=False, db_index=True, verbose_name="是否为根管理员",
                                  help_text="根管理员可以管理系统角色和权限")
    role = models.ForeignKey(
        "users.Role",

        # 如果角色仍然被用户使用，则不允许真正删除该角色
        on_delete=models.PROTECT,

        # 新注册的用户暂时可以没有角色，
        # 后续由根管理员分配
        blank=True,
        null=True,

        # 可以通过 role.users.all() 查询该角色下的用户
        related_name="users",

        verbose_name="角色",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 新增字段
    last_login = models.DateTimeField(blank=True, null=True, verbose_name="最后登录时间")

    token_version = models.PositiveIntegerField(
        default=1,
        verbose_name="Token版本",
        help_text="版本变化后，之前签发的Token立即失效",
    )

    class Meta:
        db_table = 'sys_users'
        verbose_name = '系统用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """加密密码"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        """供后面的 DRF 身份认证使用"""
        return True