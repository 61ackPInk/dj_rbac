import { createRouter, createWebHistory } from 'vue-router'

import authRoutes from './modules/auth'
import homeRoutes from './modules/home'
import testRoutes from './modules/test'
import { setupRouterGuards } from './guards'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ... 将各模块的路由数组展开，合并成完整的路由列表
    ...authRoutes,
    ...homeRoutes,
    ...testRoutes,
  ],
  scrollBehavior(to) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    }

    return { top: 0 }
  },
})

// 只在入口注册一次，不要在各模块重复注册守卫
setupRouterGuards(router)

export default router