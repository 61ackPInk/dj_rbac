import { useAuthStore } from '@/stores/auth'

// 接收路由实例，集中注册整个项目的导航规则
export const setupRouterGuards = (router) => {
  router.beforeEach((to) => {
    // 在守卫执行时获取 Store，确保 Pinia 已经注册
    const auth = useAuthStore()

    // 本地没有 Token 时，需要登录的页面跳转到登录页
    // Token 是否有效、用户有没有权限，仍由后端校验
    if (to.meta.requiresAuth && !auth.isLoggedIn) {
      return { name: 'login' }
    }

    return true
  })

  router.afterEach((to) => {
    document.title = `${to.meta.title || '页面'} - RBAC`
  })
}