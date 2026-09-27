/* ==================== 公共请求工具 ==================== */
import request from '@/utils/request'

/* ==================== 获取用户列表 ==================== */

/*
 * 根管理员获取系统中的全部用户。
 *
 * 当前后端没有分页、搜索和筛选参数，
 * 搜索与筛选由前端完成。
 */
export const getUsersApi = () => {
  return request({
    url: '/users/',
    method: 'get',
  })
}

/* ==================== 创建用户 ==================== */

/*
 * 创建新用户。
 *
 * data 包含：
 * username
 * email
 * password
 * password_confirm
 *
 * 创建成功后返回：
 * id
 * username
 * email
 */
export const createUserApi = (data) => {
  return request({
    url: '/auth/register/',
    method: 'post',
    data,
  })
}

/* ==================== 获取用户详情 ==================== */

/*
 * 根管理员根据用户 ID 获取完整用户信息。
 */
export const getUserDetailApi = (userId) => {
  return request({
    url: `/users/${userId}/`,
    method: 'get',
  })
}

/* ==================== 修改用户资料 ==================== */

/*
 * 根管理员修改指定用户的基础资料。
 *
 * 当前后端允许修改：
 * username
 * email
 * is_active
 *
 * 角色和密码不能通过这个接口修改。
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
 * 启用或禁用指定用户。
 *
 * enabled 为 true：启用账号。
 * enabled 为 false：禁用账号。
 */
export const updateUserStatusApi = (
  userId,
  enabled,
) => {
  return request({
    url: `/users/${userId}/`,
    method: 'patch',
    data: {
      is_active: enabled,
    },
  })
}

/* ==================== 分配或取消用户角色 ==================== */

/*
 * 为指定用户分配角色。
 *
 * roleId 传入角色 ID：分配角色。
 * roleId 传入 null：取消当前角色。
 *
 * 后端只允许分配当前处于启用状态的角色。
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