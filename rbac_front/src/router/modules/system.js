/*
 * ==================== 系统管理模块路由 ====================
 *
 * 这些是主布局的子路由，因此 path 不以 / 开头。
 * 数据库控制页面是否可见；这里负责把路径映射到前端视图。
 */
export default [
  // 系统概览：/system/dashboard
  {
    path: 'system/dashboard',
    name: 'system-dashboard',
    component: () => import('@/views/system/dashboard/dashboard.vue'),
    meta: {
      title: '系统概览',
      pageCode: 'SYSTEM_DASHBOARD',
    },
  },

  // 用户管理：/system/users
  {
    path: 'system/users',
    name: 'system-users',
    component: () => import('@/views/system/users/users.vue'),
    meta: {
      title: '用户管理',
      pageCode: 'SYSTEM_USERS',
    },
  },

  // 角色管理：/system/roles
  {
    path: 'system/roles',
    name: 'system-roles',
    component: () =>
      import(
        '@/views/system/roles/roles.vue'
      ),
    meta: {
      title: '角色管理',
      pageCode: 'SYSTEM_ROLES',
    },
  },
  // 页面管理：/system/pages
  {
    path: 'system/pages',
    name: 'system-pages',
    component: () =>
      import(
        '@/views/system/pages/pages.vue'
      ),
    meta: {
      title: '页面管理',
      pageCode: 'SYSTEM_PAGES',
    },
  },
]