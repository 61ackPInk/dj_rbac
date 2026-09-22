import { useAuthStore } from '@/stores/auth'
import { getVisiblePagesApi } from '@/api/pages'

// 接收路由实例，集中注册全局导航规则
export const setupRouterGuards = (router) => {
  router.beforeEach(async (to) => {
    /*
     * 在守卫执行时获取 Store。
     * 此时 main.js 已经通过 app.use(createPinia()) 注册 Pinia。
     */
    const authStore = useAuthStore()

    try {
      /*
       * 首次打开网页或刷新页面时：
       * 如果本地存在 Token，就请求 /api/auth/me/
       * 恢复当前用户信息。
       */
      await authStore.initializeAuth()
    } catch (error) {
      /*
       * 401 已经由 Store 清除了失效 Token。
       *
       * 网络故障等其他错误不在守卫里弹提示，
       * 避免每次路由切换重复出现提示。
       * 后续具体接口仍会展示相应错误。
       */
      console.warn('初始化登录状态失败：', error)
    }

    // 需要登录的页面，没有完整登录状态时进入登录页
    if (to.meta.requiresAuth && !authStore.isLoggedIn) {
      return {
        name: 'login',

        /*
         * 记录原来想访问的网址。
         * 后续可以在登录成功后返回该页面。
         */
        query: {
          redirect: to.fullPath,
        },
      }
    }
    // 有 pageCode 的页面，必须出现在当前用户的可见页面列表中
    if (to.meta.pageCode) {
      try {
        const visiblePages = await getVisiblePagesApi()
        const canAccess = visiblePages.some(
          (page) => page.code === to.meta.pageCode,
        )

        if (!canAccess) {
          return { name: 'home' }
        }
      } catch (error) {
        console.warn('检查页面权限失败：', error)
        return { name: 'home' }
      }
    }

    // 已登录用户访问登录页时，直接回到首页
    if (to.name === 'login' && authStore.isLoggedIn) {
      return {
        name: 'home',
      }
    }

    return true
  })

  router.afterEach((to) => {
    document.title =
      `${to.meta.title || '页面'} - RBAC`
  })
}