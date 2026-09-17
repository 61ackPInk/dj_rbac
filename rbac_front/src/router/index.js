import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      // 懒加载：访问页面时才加载对应组件
      component: () => import('../views/home.vue'),
      meta: {
        title: '首页',
      },
    },
  ],
})

// 页面切换后，更新浏览器标签标题
router.afterEach((to) => {
  document.title = `${to.meta.title || '页面'} - RBAC`
})

export default router