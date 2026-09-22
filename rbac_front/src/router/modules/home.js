export default [
  {
    path: '/',
    component: () => import('@/layouts/main/main-layout.vue'),
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/home/home.vue'),
        meta: {
          title: '首页',
        },
      },
      {
        path: 'system/dashboard',
        name: 'system-dashboard',
        component: () =>
          import('@/views/system/dashboard/dashboard.vue'),
        meta: {
          title: '数据概览',
        },
      },
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

// export default [
//   {
//     path: '/',
//     name: 'home',
//     component: () => import('@/views/home/home.vue'),
//     meta: {
//       title: '首页',
//       requiresAuth: true,
//     },
//   },
//   /*
//      * 以后新增页面，重复以下步骤：
//      * 1. 在 src/views 创建对应的 .vue 文件。
//      * 2. 在 routes 添加 path、唯一 name 和 component。
//      * 3. 填写 meta.title。
//      * 4. 需要登录的页面设置 requiresAuth: true。
//      *
//      * requiresAuth 只控制登录入口，不是角色权限校验。
//      * 页面和卡片权限后续按后端返回的授权配置处理。
//      */
// ]