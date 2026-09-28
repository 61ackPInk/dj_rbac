/* ==================== 请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取角色列表 ==================== */

/*
 * 获取系统中的全部角色。
 *
 * 权限：
 * 所有已登录用户都可以访问。
 *
 * 返回顺序由后端 Role 模型控制：
 * 先按照 rank 从高到低，
 * 权重相同时按照 id 从小到大。
 */
export const getRolesApi = () => {
  return request({
    url: '/roles/',
    method: 'get',
  })
}

/* ==================== 创建角色 ==================== */

/*
 * 创建一个新角色。
 *
 * 权限：
 * 只有根管理员可以访问。
 *
 * data 格式：
 * {
 *   name: '系统管理员',
 *   code: 'SYSTEM_ADMIN',
 *   rank: 100,
 *   description: '负责系统基础管理',
 *   is_active: true,
 * }
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
 * 根据角色 ID 获取完整角色信息。
 *
 * 权限：
 * 所有已登录用户都可以访问。
 */
export const getRoleDetailApi = (roleId) => {
  return request({
    url: `/roles/${roleId}/`,
    method: 'get',
  })
}

/* ==================== 修改角色 ==================== */

/*
 * 局部修改指定角色。
 *
 * 权限：
 * 只有根管理员可以访问。
 *
 * 使用 PATCH，前端只需要提交发生修改的字段，
 * 不要求每次都提交全部角色数据。
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

/* ==================== 停用角色 ==================== */

/*
 * 停用指定角色。
 *
 * 后端虽然使用 DELETE 请求，
 * 但不会真正删除数据库记录，
 * 只会把 is_active 修改为 false。
 */
export const disableRoleApi = (roleId) => {
  return request({
    url: `/roles/${roleId}/`,
    method: 'delete',
  })
}

/* ==================== 启用角色 ==================== */

/*
 * 重新启用已经停用的角色。
 *
 * 后端没有单独的“启用角色”接口，
 * 因此使用角色修改接口更新 is_active。
 */
export const enableRoleApi = (roleId) => {
  return request({
    url: `/roles/${roleId}/`,
    method: 'patch',
    data: {
      is_active: true,
    },
  })
}