/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取系统概览 ==================== */

/*
 * 获取系统中的用户、角色、页面和最近用户统计。
 * 页面直接获得后端统一响应中的 data。
 */
export const getSystemOverviewApi = () => {
  return request({
    url: '/dashboards/system/overview/',
    method: 'get',
  })
}
