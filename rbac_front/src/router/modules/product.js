/*
 * ==================== 商品模块路由 ====================
 *
 * 商品模块页面是主布局的子路由，
 * 因此 path 不以 / 开头。
 *
 * 后端页面数据决定菜单是否显示，
 * 当前文件负责把页面路径映射到真实 Vue 组件。
 */
export default [
  /* ==================== 商品列表 ==================== */

  {
    path: 'product/list',
    name: 'product-list',
    component: () =>
      import(
        '@/views/product/list/product-list.vue'
      ),
    meta: {
      title: '商品列表',
      pageCode: 'PRODUCT_LIST',
    },
  },
]