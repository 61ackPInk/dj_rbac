// 认证模块的路由：以后注册、找回密码页面也放在这里
export default [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/login/login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
    },
  },
]