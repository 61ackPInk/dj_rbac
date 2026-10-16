import request from '@/utils/request'

/**
 * 获取商品仓库列表
 *
 * 后端权限：
 * - PRODUCT_LIST
 * - PRODUCT_BUNDLE_LIST
 * 拥有任意一个即可访问。
 */
export function getProductWarehousesApi() {
  return request({
    url: '/products/warehouses/',
    method: 'get',
  })
}

/**
 * 获取商品组合列表
 *
 * @param {Object} params 查询参数
 * @param {string} params.warehouse_code 仓库编码，必填
 * @param {number} [params.page=1] 页码
 * @param {number} [params.page_size=20] 每页数量
 * @param {string} [params.bundle_sku] 后端组合 SKU 模糊查询
 * @param {string} [params.name] 后端名称模糊查询
 */
export function getProductBundlesApi(params) {
  return request({
    url: '/products/bundles/',
    method: 'get',
    params,
  })
}