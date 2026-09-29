/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取角色列表 ==================== */

/*
 * 获取系统中的全部角色。
 *
 * 所需操作权限：
 * ROLE_LIST
 */
export const getRolesApi = () => {
  return request({
    url: '/roles/',
    method: 'get',
  })
}

/* ==================== 创建角色 ==================== */

/*
 * 创建角色。
 *
 * 所需操作权限：
 * ROLE_CREATE
 */
export const createRoleApi = (data) => {
  return request({
    url: '/roles/',
    method: 'post',
    data,
  })
}

/* ==================== 获取角色详情 ==================== */

/*
 * 获取指定角色的完整资料。
 *
 * 所需操作权限：
 * ROLE_DETAIL
 */
export const getRoleDetailApi = (
  roleId,
) => {
  return request({
    url: `/roles/${roleId}/`,
    method: 'get',
  })
}

/* ==================== 修改角色资料 ==================== */

/*
 * 修改角色名称、编码、权重和描述。
 *
 * 所需操作权限：
 * ROLE_UPDATE
 *
 * 注意：
 * 不能通过这个接口修改 is_active。
 */
export const updateRoleApi = (
  roleId,
  data,
) => {
  return request({
    url: `/roles/${roleId}/`,
    method: 'patch',
    data,
  })
}

/* ==================== 修改角色状态 ==================== */

/*
 * 启用或停用指定角色。
 *
 * 所需操作权限：
 * ROLE_CHANGE_STATUS
 */
export const updateRoleStatusApi = (
  roleId,
  isActive,
) => {
  return request({
    url: `/roles/${roleId}/status/`,
    method: 'patch',
    data: {
      is_active: isActive,
    },
  })
}

/* ==================== 停用角色 ==================== */

/*
 * 保留当前页面正在使用的函数名称，
 * 避免业务页面在本步骤立即报错。
 *
 * 后续角色页面改造完成后，
 * 可以直接统一使用 updateRoleStatusApi。
 */
export const disableRoleApi = (
  roleId,
) => {
  return updateRoleStatusApi(
    roleId,
    false,
  )
}

/* ==================== 启用角色 ==================== */

export const enableRoleApi = (
  roleId,
) => {
  return updateRoleStatusApi(
    roleId,
    true,
  )
}

/* ==================== 获取角色操作权限 ==================== */

/*
 * 获取指定角色当前拥有的操作权限。
 *
 * 只有根管理员可以访问。
 */
export const getRolePermissionsApi = (
  roleId,
) => {
  return request({
    url: `/roles/${roleId}/permissions/`,
    method: 'get',
  })
}

/* ==================== 配置角色操作权限 ==================== */

/*
 * 替换指定角色的全部操作权限。
 *
 * 只有根管理员可以访问。
 *
 * permissionIds 示例：
 * [1, 2, 3]
 */
export const updateRolePermissionsApi = (
  roleId,
  permissionIds,
) => {
  return request({
    url: `/roles/${roleId}/permissions/`,
    method: 'patch',
    data: {
      permission_ids: permissionIds,
    },
  })
}