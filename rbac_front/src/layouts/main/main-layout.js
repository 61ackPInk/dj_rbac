/* ==================== Vue 相关依赖 ==================== */
import {
  computed,
  defineComponent,
  onBeforeUnmount,
  onMounted,
  ref,
  watch,
} from 'vue'

import {
  RouterLink,
  RouterView,
  useRoute,
  useRouter,
} from 'vue-router'

/* ==================== 项目内部依赖 ==================== */
import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { message } from '@/utils/message'

/* ==================== 响应式断点 ==================== */

/*
 * 与后台布局样式中的手机端断点保持一致。
 */
const MOBILE_BREAKPOINT = 760

export default defineComponent({
  name: 'MainLayout',

  components: {
    RouterLink,
    RouterView,
  },

  setup() {
    /* ==================== 路由与状态仓库 ==================== */
    const route = useRoute()
    const router = useRouter()

    const authStore = useAuthStore()
    const navigationStore = useNavigationStore()

    /* ==================== 布局状态 ==================== */

    // 电脑端侧边栏是否处于折叠状态
    const sidebarCollapsed = ref(false)

    // 手机端侧边栏是否已经打开
    const mobileSidebarOpen = ref(false)

    // 右上角用户菜单是否已经打开
    const userMenuOpen = ref(false)

    // 是否正在退出登录
    const logoutLoading = ref(false)

    /* ==================== 当前设备判断 ==================== */

    /*
     * 这里只在用户触发操作时读取窗口宽度，
     * 不需要额外维护响应式窗口尺寸状态。
     */
    const isMobile = () => {
      return window.innerWidth <= MOBILE_BREAKPOINT
    }

    /* ==================== 侧边栏控制 ==================== */

    /*
     * 电脑端点击时切换折叠状态；
     * 手机端点击时切换抽屉状态。
     */
    const toggleSidebar = () => {
      userMenuOpen.value = false

      if (isMobile()) {
        mobileSidebarOpen.value =
          !mobileSidebarOpen.value

        return
      }

      sidebarCollapsed.value =
        !sidebarCollapsed.value
    }

    // 关闭手机端侧边栏
    const closeMobileSidebar = () => {
      mobileSidebarOpen.value = false
    }

    /* ==================== 用户菜单控制 ==================== */

    // 切换右上角用户菜单
    const toggleUserMenu = () => {
      userMenuOpen.value = !userMenuOpen.value
    }

    // 关闭右上角用户菜单
    const closeUserMenu = () => {
      userMenuOpen.value = false
    }

    /*
     * 点击用户菜单内部时阻止事件冒泡，
     * 避免 document 的点击事件立即关闭菜单。
     */
    const stopUserMenuPropagation = (event) => {
      event.stopPropagation()
    }

    /* ==================== 全局键盘与窗口事件 ==================== */

    /*
     * 按下 Escape 时关闭用户菜单和手机侧边栏。
     */
    const handleDocumentKeydown = (event) => {
      if (event.key !== 'Escape') {
        return
      }

      closeUserMenu()
      closeMobileSidebar()
    }

    /*
     * 从手机端切换回电脑端时，
     * 清除手机抽屉残留的打开状态。
     */
    const handleWindowResize = () => {
      if (!isMobile()) {
        closeMobileSidebar()
      }
    }

    /* ==================== 后端动态菜单 ==================== */

    /*
     * 后端返回的根页面作为菜单分组，
     * 根页面的直接子页面作为该分组下的菜单项。
     *
     * 示例：
     *
     * 系统管理
     * ├── 系统概览
     * ├── 用户管理
     * └── 角色管理
     */
    const menuGroups = computed(() => {
      return navigationStore.topMenus
        .filter((menu) => menu.path !== '/')
        .map((menu) => {
          return {
            ...menu,
            children:
              navigationStore.getChildMenus(menu.id),
          }
        })
    })

    /*
     * 当前路由是否选中了指定菜单。
     *
     * 除了完全相等，也允许子路由保持父菜单选中：
     * /system/users/list 会继续选中 /system/users。
     */
    const isMenuActive = (menuPath) => {
      if (!menuPath) {
        return false
      }

      if (route.path === menuPath) {
        return true
      }

      return route.path.startsWith(`${menuPath}/`)
    }

    /* ==================== 页面标题与面包屑 ==================== */

    /*
     * 优先使用路由配置中的 title；
     * 没有配置时，再使用当前后端页面名称。
     */
    const currentPageName = computed(() => {
      if (route.path === '/') {
        return '首页'
      }

      const currentPage =
        navigationStore.pages.find((page) => {
          return page.path === route.path
        })

      return (
        route.meta.title ||
        currentPage?.name ||
        '当前页面'
      )
    })

    /*
     * 查找当前页面所属的根菜单，
     * 用于生成顶部面包屑。
     */
    const currentMenuGroup = computed(() => {
      if (route.path === '/') {
        return null
      }

      const currentPage =
        navigationStore.pages.find((page) => {
          return (
            page.path === route.path ||
            route.path.startsWith(`${page.path}/`)
          )
        })

      if (!currentPage) {
        return null
      }

      if (currentPage.parent_id == null) {
        return currentPage
      }

      return navigationStore.topMenus.find((menu) => {
        return menu.id === currentPage.parent_id
      })
    })

    /* ==================== 当前用户信息 ==================== */

    const username = computed(() => {
      return authStore.user?.username || '用户'
    })

    /*
     * 优先显示昵称，否则显示用户名。
     */
    const userDisplayName = computed(() => {
      return (
        authStore.user?.nickname ||
        authStore.user?.name ||
        username.value
      )
    })

    /*
     * 当前没有统一角色名称字段时，
     * 先根据超级管理员状态显示身份。
     */
    const userRoleName = computed(() => {
      if (authStore.user?.is_superuser) {
        return 'Administrator'
      }

      return 'User'
    })

    /*
     * 用户头像使用显示名称的第一个字符。
     */
    const userInitial = computed(() => {
      return userDisplayName.value
        .trim()
        .charAt(0)
        .toUpperCase() || '用'
    })

    /* ==================== 暂未开放功能 ==================== */

    const showUnavailable = (featureName) => {
      closeUserMenu()
      message.info(`${featureName}功能暂未开放`)
    }

    /* ==================== 退出登录 ==================== */

    const handleLogout = async () => {
      if (logoutLoading.value) {
        return
      }

      logoutLoading.value = true

      try {
        await authStore.logout()

        message.success('退出登录成功')

        /*
         * 使用 replace，避免浏览器返回按钮
         * 再次回到退出前的后台页面。
         */
        await router.replace({
          name: 'login',
        })
      } catch (error) {
        message.error(
          error.userMessage ||
          '退出登录失败，请稍后重试',
        )
      } finally {
        logoutLoading.value = false
        closeUserMenu()
      }
    }

    /* ==================== 路由变化处理 ==================== */

    /*
     * 切换页面后自动关闭手机侧边栏和用户菜单。
     */
    watch(
      () => route.fullPath,
      () => {
        closeMobileSidebar()
        closeUserMenu()
      },
    )

    /* ==================== 初始化布局 ==================== */

    onMounted(async () => {
      document.addEventListener(
        'click',
        closeUserMenu,
      )

      document.addEventListener(
        'keydown',
        handleDocumentKeydown,
      )

      window.addEventListener(
        'resize',
        handleWindowResize,
      )

      try {
        await navigationStore.loadPages()
      } catch (error) {
        message.error(
          error.userMessage ||
          '导航菜单加载失败',
        )
      }
    })

    /* ==================== 清理全局事件 ==================== */

    onBeforeUnmount(() => {
      document.removeEventListener(
        'click',
        closeUserMenu,
      )

      document.removeEventListener(
        'keydown',
        handleDocumentKeydown,
      )

      window.removeEventListener(
        'resize',
        handleWindowResize,
      )
    })

    /* ==================== 向模板暴露内容 ==================== */

    return {
      route,

      sidebarCollapsed,
      mobileSidebarOpen,
      userMenuOpen,
      logoutLoading,

      menuGroups,
      currentPageName,
      currentMenuGroup,

      username,
      userDisplayName,
      userRoleName,
      userInitial,

      toggleSidebar,
      closeMobileSidebar,
      toggleUserMenu,
      stopUserMenuPropagation,
      isMenuActive,
      showUnavailable,
      handleLogout,
    }
  },
})