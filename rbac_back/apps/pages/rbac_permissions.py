"""
-*- coding: utf-8 -*-
@File  : rbac_permissions.py
@Author: 61ackPink
@Time : 2026/10/16
@Desc : 页面系统内置操作权限配置
"""


# ==================== 页面操作权限 ====================

PERMISSION_CONFIG = {
    "SYSTEM_PAGES": [
        {
            "name": "查看页面列表",
            "code": "PAGE_LIST",
            "description": "允许查看系统页面列表",
            "sort_order": 10,
        },
        {
            "name": "查看页面详情",
            "code": "PAGE_DETAIL",
            "description": "允许查看指定页面的详细信息",
            "sort_order": 20,
        },
        {
            "name": "创建页面",
            "code": "PAGE_CREATE",
            "description": "允许创建新的系统页面",
            "sort_order": 30,
        },
        {
            "name": "修改页面资料",
            "code": "PAGE_UPDATE",
            "description": (
                "允许修改页面名称、路由、组件和父页面等资料"
            ),
            "sort_order": 40,
        },
        {
            "name": "修改页面状态",
            "code": "PAGE_CHANGE_STATUS",
            "description": "允许启用或停用页面",
            "sort_order": 50,
        },
        {
            "name": "分配页面角色",
            "code": "PAGE_ASSIGN_ROLE",
            "description": "允许配置页面对哪些角色可见",
            "sort_order": 60,
        },
    ],
}
