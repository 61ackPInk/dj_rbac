/* ==================== 请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取当前用户可见页面 ==================== */

/*
 * 登录后加载顶部导航和侧边栏时使用。
 */
export const getVisiblePagesApi = () => {
  return request({
    url: '/pages/visible/',
    method: 'get',
  })
}

/* ==================== 获取全部页面 ==================== */

/*
 * 页面管理列表使用。
 *
 * 返回启用和停用的全部页面，
 * 只有根管理员可以访问。
 */
export const getPagesApi = () => {
  return request({
    url: '/pages/',
    method: 'get',
  })
}

/* ==================== 创建页面 ==================== */

/*
 * data 可包含：
 *
 * name
 * code
 * path
 * component
 * icon
 * parent_id
 * visible_role_ids
 * sort_order
 * is_active
 */
export const createPageApi = (data) => {
  return request({
    url: '/pages/',
    method: 'post',
    data,
  })
}

/* ==================== 获取页面详情 ==================== */

export const getPageDetailApi = (pageId) => {
  return request({
    url: `/pages/${pageId}/`,
    method: 'get',
  })
}

/* ==================== 修改页面 ==================== */

/*
 * 使用 PATCH 局部修改页面，
 * 同时支持修改父页面和可见角色。
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

/* ==================== 停用页面 ==================== */

/*
 * 后端不会真正删除页面，
 * 只会将 is_active 修改为 false。
 */
export const disablePageApi = (pageId) => {
  return request({
    url: `/pages/${pageId}/`,
    method: 'delete',
  })
}

/* ==================== 启用页面 ==================== */

/*
 * 后端没有独立的启用接口，
 * 使用 PATCH 恢复页面状态。
 */
export const enablePageApi = (pageId) => {
  return request({
    url: `/pages/${pageId}/`,
    method: 'patch',
    data: {
      is_active: true,
    },
  })
}