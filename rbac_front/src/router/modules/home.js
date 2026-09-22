import systemRoutes from './system'

/* ==================== 登录后的主布局 ==================== */
export default [
  {
    path: '/',
    component: () => import('@/layouts/main/main-layout.vue'),
    meta: {
      requiresAuth: true,
    },

    children: [
      /* ==================== 固定首页 ==================== */
      {
        path: '',
        name: 'home',
        component: () => import('@/views/home/home.vue'),
        meta: {
          title: '首页',
        },
      },

      /* ==================== 业务模块路由 ==================== */
      ...systemRoutes,

      /* ==================== 尚未开发的页面 ==================== */
      // 必须放在最后，避免抢先匹配业务模块的路径
      {
        path: ':pathMatch(.*)*',
        name: 'page-placeholder',
        component: () =>
          import('@/views/common/page-placeholder.vue'),
        meta: {
          title: '待开发页面',
        },
      },
    ],
  },
]