/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取用户列表 ==================== */

/*
 * 获取系统中的用户列表。
 *
 * 所需操作权限：
 * USER_LIST
 */
export const getUsersApi = () => {
  return request({
    url: '/users/',
    method: 'get',
  })
}

/* ==================== 创建用户 ==================== */

/*
 * 通过用户管理接口创建普通用户。
 *
 * 所需操作权限：
 * USER_CREATE
 *
 * 注意：
 * 管理员创建用户不能继续使用公开注册接口。
 *
 * data 示例：
 * {
 *   username: 'example',
 *   email: 'example@test.com',
 *   password: 'password',
 *   password_confirm: 'password',
 * }
 */
export const createUserApi = (data) => {
  return request({
    url: '/users/',
    method: 'post',
    data,
  })
}

/* ==================== 获取用户详情 ==================== */

/*
 * 获取指定用户的完整资料。
 *
 * 所需操作权限：
 * USER_DETAIL
 */
export const getUserDetailApi = (
  userId,
) => {
  return request({
    url: `/users/${userId}/`,
    method: 'get',
  })
}

/* ==================== 修改用户资料 ==================== */

/*
 * 修改指定用户的基础资料。
 *
 * 所需操作权限：
 * USER_UPDATE
 *
 * 当前接口只负责：
 * username
 * email
 *
 * 不通过该接口修改状态、角色和密码。
 */
export const updateUserApi = (
  userId,
  data,
) => {
  return request({
    url: `/users/${userId}/`,
    method: 'patch',
    data,
  })
}

/* ==================== 修改用户状态 ==================== */

/*
 * 启用或停用指定用户。
 *
 * 所需操作权限：
 * USER_CHANGE_STATUS
 */
export const updateUserStatusApi = (
  userId,
  isActive,
) => {
  return request({
    url: `/users/${userId}/status/`,
    method: 'patch',
    data: {
      is_active: isActive,
    },
  })
}

/* ==================== 分配用户角色 ==================== */

/*
 * 为指定用户分配或取消角色。
 *
 * 所需操作权限：
 * USER_ASSIGN_ROLE
 *
 * roleId 为角色 ID：分配角色。
 * roleId 为 null：取消当前角色。
 */
export const assignUserRoleApi = (
  userId,
  roleId,
) => {
  return request({
    url: `/users/${userId}/role/`,
    method: 'patch',
    data: {
      role_id: roleId,
    },
  })
}

/* ==================== 重置用户密码 ==================== */

/*
 * 管理员重置指定普通用户的密码。
 *
 * 所需操作权限：
 * USER_RESET_PASSWORD
 *
 * data 的具体密码字段沿用后端接口定义。
 */
export const resetUserPasswordApi = (
  userId,
  data,
) => {
  return request({
    url: `/users/${userId}/password/`,
    method: 'patch',
    data,
  })
}