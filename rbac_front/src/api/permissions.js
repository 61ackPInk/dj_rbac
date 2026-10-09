/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/*
 * 权限定义管理接口全部只允许根管理员使用。
 *
 * 普通角色管理员即使拥有角色管理页面权限，
 * 也不能创建权限定义或给角色增加权限。
 */

/* ==================== 获取权限列表 ==================== */

export const getPermissionsApi = () => {
  return request({
    url: '/permissions/',
    method: 'get',
  })
}

/* ==================== 创建权限定义 ==================== */

export const createPermissionApi = (
  data,
) => {
  return request({
    url: '/permissions/',
    method: 'post',
    data,
  })
}

/* ==================== 获取权限详情 ==================== */

export const getPermissionDetailApi = (
  permissionId,
) => {
  return request({
    url: `/permissions/${permissionId}/`,
    method: 'get',
  })
}

/* ==================== 修改权限定义 ==================== */

export const updatePermissionApi = (
  permissionId,
  data,
) => {
  return request({
    url: `/permissions/${permissionId}/`,
    method: 'patch',
    data,
  })
}

/* ==================== 停用权限定义 ==================== */

/*
 * DELETE 只会软停用权限，
 * 不会真正删除数据库记录。
 */
export const disablePermissionApi = (
  permissionId,
) => {
  return request({
    url: `/permissions/${permissionId}/`,
    method: 'delete',
  })
}