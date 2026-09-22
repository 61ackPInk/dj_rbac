import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { message } from '@/utils/message'

/* ==================== 固定的首页菜单 ==================== */
const homeMenu = {
  id: 'home',
  name: '首页',
  path: '/',
}

const homeSideMenus = [
  { id: 'home-overview', name: '概览', path: '/#overview', icon: 'bi bi-house' },
  { id: 'home-account', name: '我的账号', path: '/#account', icon: 'bi bi-person' },
]

export default defineComponent({
  name: 'MainLayout',
  components: { RouterLink, RouterView },

  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    const navigationStore = useNavigationStore()

    /* ==================== 手机端抽屉菜单 ==================== */
    const mobileMenuOpen = ref(false)

    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value
    }

    const closeMobileMenu = () => {
      mobileMenuOpen.value = false
    }

    // 切换页面或首页定位点后，自动收起手机菜单
    watch(() => route.fullPath, closeMobileMenu)

    /* ==================== 顶部导航与当前用户 ==================== */
    const username = computed(
      () => authStore.user?.username || '用户',
    )

    // const topMenus = computed(() => [
    //   homeMenu,
    //   ...navigationStore.topMenus.filter((menu) => menu.path !== '/'),
    // ])
    const topMenus = computed(() => [
      homeMenu,
      ...navigationStore.topMenus
        .filter((menu) => menu.path !== '/')
        .map((menu) => {
          // getChildMenus 已按 sort_order 排序，且只包含当前用户可见页面
          const firstChild = navigationStore.getChildMenus(menu.id)[0]

          return {
            ...menu,
            entryPath: firstChild?.path || menu.path,
          }
        }),
    ])



    // 根据当前页面，确定选中的顶部菜单
    const activeTopMenu = computed(() => {
      if (route.path === '/') return homeMenu

      const currentPage = navigationStore.pages.find(
        (page) => page.path === route.path,
      )

      const topId = currentPage?.parent_id ?? currentPage?.id

      return navigationStore.topMenus.find(
        (menu) => menu.id === topId,
      )
    })

    /*
     * 预留：以后使用三级菜单时，可恢复沿 parent_id
     * 向上查找根页面的逻辑；目前保持两级菜单。
     *
     * const activeTopMenu = computed(() => {
     *   if (route.path === '/') return homeMenu
     *
     *   let currentPage = navigationStore.pages.find(
     *     (page) => page.path === route.path,
     *   )
     *
     *   const visited = new Set()
     *
     *   while (currentPage?.parent_id != null) {
     *     if (visited.has(currentPage.id)) return null
     *     visited.add(currentPage.id)
     *
     *     currentPage = navigationStore.pages.find(
     *       (page) => page.id === currentPage.parent_id,
     *     )
     *   }
     *
     *   if (!currentPage) return null
     *
     *   return navigationStore.topMenus.find(
     *     (menu) => menu.id === currentPage.id,
     *   )
     * })
     */

    /* ==================== 左侧侧边栏 ==================== */
    const sideMenus = computed(() => {
      // 首页使用固定入口，不依赖数据库
      if (route.path === '/') return homeSideMenus

      // 其他页面使用接口返回的子菜单
      if (!activeTopMenu.value) return []
      return navigationStore.getChildMenus(activeTopMenu.value.id)
    })

    /* ==================== 加载后台菜单 ==================== */
    onMounted(async () => {
      try {
        await navigationStore.loadPages()
      } catch (error) {
        message.error(error.userMessage || '导航菜单加载失败')
      }
    })

    /* ==================== 提供给页面模板 ==================== */
    return {
      route,
      username,
      topMenus,
      activeTopMenu,
      sideMenus,
      mobileMenuOpen,
      toggleMobileMenu,
      closeMobileMenu,
    }
  },
})