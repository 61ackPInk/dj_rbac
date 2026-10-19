"""
-*- coding: utf-8 -*-
@File  : rbac_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 用户与角色系统内置操作权限配置
"""


# ==================== 用户与角色操作权限 ====================

PERMISSION_CONFIG = {
    "SYSTEM_USERS": [
        {
            "name": "查看用户列表",
            "code": "USER_LIST",
            "description": "允许查看系统用户列表",
            "sort_order": 10,
        },
        {
            "name": "查看用户详情",
            "code": "USER_DETAIL",
            "description": "允许查看指定用户的详细信息",
            "sort_order": 20,
        },
        {
            "name": "创建用户",
            "code": "USER_CREATE",
            "description": "允许通过用户管理接口创建用户",
            "sort_order": 30,
        },
        {
            "name": "修改用户资料",
            "code": "USER_UPDATE",
            "description": "允许修改普通用户的用户名和邮箱",
            "sort_order": 40,
        },
        {
            "name": "修改用户状态",
            "code": "USER_CHANGE_STATUS",
            "description": "允许启用或停用普通用户",
            "sort_order": 50,
        },
        {
            "name": "分配用户角色",
            "code": "USER_ASSIGN_ROLE",
            "description": "允许给普通用户分配或取消角色",
            "sort_order": 60,
        },
        {
            "name": "重置用户密码",
            "code": "USER_RESET_PASSWORD",
            "description": "允许重置普通用户密码",
            "sort_order": 70,
        },
    ],
    "SYSTEM_ROLES": [
        {
            "name": "查看角色列表",
            "code": "ROLE_LIST",
            "description": "允许查看系统角色列表",
            "sort_order": 10,
        },
        {
            "name": "查看角色详情",
            "code": "ROLE_DETAIL",
            "description": "允许查看指定角色的详细信息",
            "sort_order": 20,
        },
        {
            "name": "创建角色",
            "code": "ROLE_CREATE",
            "description": "允许创建新的系统角色",
            "sort_order": 30,
        },
        {
            "name": "修改角色资料",
            "code": "ROLE_UPDATE",
            "description": (
                "允许修改角色名称、编码、权重和描述"
            ),
            "sort_order": 40,
        },
        {
            "name": "修改角色状态",
            "code": "ROLE_CHANGE_STATUS",
            "description": "允许启用或停用角色",
            "sort_order": 50,
        },
    ],
}
