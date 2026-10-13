/* ==================== 公共请求工具 ==================== */

import request from '@/utils/request'

/* ==================== 获取商品列表 ==================== */

/*
 * 获取 ERP 商品及其库存信息。
 *
 * 所需操作权限：
 * PRODUCT_LIST
 *
 * params 支持：
 * {
 *   page,
 *   page_size,
 *   customer_sku,
 *   category_id,
 *   created_at_from,
 *   created_at_to,
 * }
 *
 * request.js 会自动：
 * 1. 携带当前系统的 JWT；
 * 2. 处理 Access Token 刷新；
 * 3. 取出统一响应结构中的 data。
 *
 * 前端不直接访问元仓，也不接触元仓密钥。
 */
export const getProductsApi = (params = {}) => {
  return request({
    url: '/products/',
    method: 'get',
    params,
  })
}

/* ==================== 获取商品详情 ==================== */

/*
 * 根据客户 SKU 获取商品详情。
 *
 * 所需操作权限：
 * PRODUCT_DETAIL
 *
 * encodeURIComponent 用于安全处理 SKU 中可能存在的
 * 空格、斜杠之外的特殊字符，避免破坏请求地址。
 */
export const getProductDetailApi = (
  customerSku,
) => {
  return request({
    url:
      `/products/by-sku/` +
      `${encodeURIComponent(customerSku)}/`,
    method: 'get',
  })
}