"""
-*- coding: utf-8 -*-
@File  : operations.py
@Author: 61ackPink
@Time : 2026/9/28 17:26
@Desc : 操作权限校验
"""

from rest_framework.permissions import BasePermission


class HasOperationPermission(BasePermission):
    """
    检查当前用户是否拥有指定操作权限。

    业务视图需要通过 required_permissions
    声明不同请求方法对应的权限编码。

    例如：

    required_permissions = {
        "GET": "USER_LIST",
        "POST": "USER_CREATE",
    }
    """

    message = "你没有执行此操作的权限"

    def has_permission(self, request, view):
        """在进入业务视图前检查操作权限"""

        user = request.user

        # --------------------
        # 检查用户登录状态
        # --------------------

        if not getattr(
            user,
            "is_authenticated",
            False,
        ):
            return False

        # 已经停用的账号不能继续操作
        if not getattr(
            user,
            "is_active",
            False,
        ):
            return False

        # --------------------
        # 获取当前接口要求的权限
        # --------------------

        required_permissions = getattr(
            view,
            "required_permissions",
            {},
        )

        permission_code = (
            required_permissions.get(
                request.method,
            )
        )

        # 视图没有声明权限编码时直接拒绝。
        #
        # 这样可以避免开发新接口时，
        # 忘记配置权限而造成越权。
        if not permission_code:
            return False

        # --------------------
        # 根管理员直接放行
        # --------------------

        # 根管理员不需要逐个分配操作权限，
        # 但视图仍然必须声明 required_permissions。
        if getattr(
            user,
            "is_root",
            False,
        ):
            return True

        # --------------------
        # 检查普通用户角色
        # --------------------

        role = getattr(
            user,
            "role",
            None,
        )

        # 普通用户必须拥有角色
        if role is None:
            return False

        # 角色已经停用时不能继续使用权限
        if not role.is_active:
            return False

        # --------------------
        # 检查页面与操作权限
        # --------------------

        return role.permissions.filter(
            # 角色必须拥有当前接口需要的权限
            code=permission_code,

            # 操作权限必须处于启用状态
            is_active=True,

            # 权限所属页面必须处于启用状态
            page__is_active=True,

            # 当前角色还必须拥有权限所属页面
            page__visible_roles=role,
        ).exists()



"""
GET /api/users/
    └─ 需要 USER_LIST

POST /api/users/
    └─ 需要 USER_CREATE

# 同时存在查询和修改的详情接口
class UserDetailAPIView(GenericAPIView):
    # 用户详情和修改接口

    permission_classes = [
        HasOperationPermission,
    ]

    required_permissions = {
        "GET": "USER_DETAIL",
        "PATCH": "USER_UPDATE",
    }
 

# 普通用户必须同时满足：
账号启用
  +
角色启用
  +
页面启用
  +
角色拥有该页面
  +
操作权限启用
  +
角色拥有该操作权限
"""