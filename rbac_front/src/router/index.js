import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/login.vue'),
      meta: {
        title: '登录',
        requiresAuth: false,
      },
    },
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/home.vue'),
      meta: {
        title: '首页',
        requiresAuth: true,
      },
    },

    /*
     * 以后新增页面，重复以下步骤：
     * 1. 在 src/views 创建对应的 .vue 文件。
     * 2. 在 routes 添加 path、唯一 name 和 component。
     * 3. 填写 meta.title。
     * 4. 需要登录的页面设置 requiresAuth: true。
     *
     * requiresAuth 只控制登录入口，不是角色权限校验。
     * 页面和卡片权限后续按后端返回的授权配置处理。
     */
  ],
})

// 每次进入路由前执行
router.beforeEach((to) => {
  // 在守卫内部获取 Store，确保 main.js 已经注册 Pinia。
  // 不要在文件顶层直接调用 useAuthStore()。
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'login' }
  }

  return true
})

router.afterEach((to) => {
  document.title = `${to.meta.title || '页面'} - RBAC`
})

export default router