/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取当前用户可见页面 ==================== */

/*
 * 获取当前用户能够访问的页面。
 *
 * 用于：
 * 顶部导航、侧边栏和路由权限判断。
 */
export const getVisiblePagesApi = () => {
  return request({
    url: '/pages/visible/',
    method: 'get',
  })
}

/* ==================== 获取全部页面 ==================== */

/*
 * 获取页面管理列表。
 *
 * 所需操作权限：
 * PAGE_LIST
 */
export const getPagesApi = () => {
  return request({
    url: '/pages/',
    method: 'get',
  })
}

/* ==================== 创建页面 ==================== */

/*
 * 创建页面基础资料。
 *
 * 所需操作权限：
 * PAGE_CREATE
 *
 * 注意：
 * 不能再提交 visible_role_ids。
 * 页面角色需要创建成功后单独配置。
 */
export const createPageApi = (data) => {
  return request({
    url: '/pages/',
    method: 'post',
    data,
  })
}

/* ==================== 获取页面详情 ==================== */

/*
 * 获取指定页面的完整资料。
 *
 * 所需操作权限：
 * PAGE_DETAIL
 */
export const getPageDetailApi = (
  pageId,
) => {
  return request({
    url: `/pages/${pageId}/`,
    method: 'get',
  })
}

/* ==================== 修改页面资料 ==================== */

/*
 * 修改页面基础资料。
 *
 * 所需操作权限：
 * PAGE_UPDATE
 *
 * 不能通过这个接口修改：
 * is_active
 * visible_role_ids
 */
export const updatePageApi = (
  pageId,
  data,
) => {
  return request({
    url: `/pages/${pageId}/`,
    method: 'patch',
    data,
  })
}

/* ==================== 修改页面状态 ==================== */

/*
 * 启用或停用指定页面。
 *
 * 所需操作权限：
 * PAGE_CHANGE_STATUS
 */
export const updatePageStatusApi = (
  pageId,
  isActive,
) => {
  return request({
    url: `/pages/${pageId}/status/`,
    method: 'patch',
    data: {
      is_active: isActive,
    },
  })
}

/* ==================== 停用页面 ==================== */

/*
 * 暂时保留旧业务页面使用的函数名称，
 * 内部改为调用新版状态接口。
 */
export const disablePageApi = (
  pageId,
) => {
  return updatePageStatusApi(
    pageId,
    false,
  )
}

/* ==================== 启用页面 ==================== */

export const enablePageApi = (
  pageId,
) => {
  return updatePageStatusApi(
    pageId,
    true,
  )
}

/* ==================== 查询页面可见角色 ==================== */

/*
 * 查询指定页面已经分配的角色。
 *
 * 所需操作权限：
 * PAGE_DETAIL
 */
export const getPageRolesApi = (
  pageId,
) => {
  return request({
    url: `/pages/${pageId}/roles/`,
    method: 'get',
  })
}

/* ==================== 配置页面可见角色 ==================== */

/*
 * 替换指定页面的全部可见角色。
 *
 * 所需操作权限：
 * PAGE_ASSIGN_ROLE
 *
 * roleIds 传入空数组时，
 * 表示清除该页面的全部可见角色。
 */
export const updatePageRolesApi = (
  pageId,
  roleIds,
) => {
  return request({
    url: `/pages/${pageId}/roles/`,
    method: 'patch',
    data: {
      role_ids: roleIds,
    },
  })
}