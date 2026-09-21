<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { message } from '@/utils/message'

const route = useRoute()
const authStore = useAuthStore()
const navigationStore = useNavigationStore()

const homeMenu = {
  id: 'home',
  name: '首页',
  path: '/',
}

const topMenus = computed(() => [
  homeMenu,
  ...navigationStore.topMenus.filter((menu) => menu.path !== '/'),
])

const mobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
}

// 切换页面后自动收起手机菜单
watch(() => route.fullPath, closeMobileMenu)


const username = computed(
  () => authStore.user?.username || '用户',
)

// 根据当前网址，找到所属的顶部菜单
const activeTopMenu = computed(() => {
  if (route.path === '/') return homeMenu

  let currentPage = navigationStore.pages.find(
    (page) => page.path === route.path,
  )

  const visited = new Set()

  // 沿 parent_id 一直向上找到根页面
  while (currentPage?.parent_id != null) {
    if (visited.has(currentPage.id)) return null
    visited.add(currentPage.id)

    currentPage = navigationStore.pages.find(
      (page) => page.id === currentPage.parent_id,
    )
  }

  if (!currentPage) return null

  return navigationStore.topMenus.find(
    (menu) => menu.id === currentPage.id,
  )
})

// 左侧只显示当前顶部菜单下的页面
const sideMenus = computed(() => {
  if (!activeTopMenu.value) return []
  return navigationStore.getChildMenus(activeTopMenu.value.id)
})

onMounted(async () => {
  try {
    await navigationStore.loadPages()

  } catch (error) {
    message.error(error.userMessage || '导航菜单加载失败')
  }
})
</script>

<template>
  <div class="main-layout">
    <header class="layout-header">
      <!-- 手机端菜单按钮 -->
      <button type="button" class="mobile-menu-button" :aria-label="mobileMenuOpen ? '关闭侧边菜单' : '打开侧边菜单'"
        aria-controls="mobile-sidebar" :aria-expanded="mobileMenuOpen" @click="toggleMobileMenu">
        <i class="bi bi-list" aria-hidden="true"></i>
      </button>

      <div class="header-brand">
        <!-- <span class="brand-mark" aria-hidden="true"></span> -->
        <span class="logo-dot"></span>
        <span>RBAC 管理系统</span>
      </div>

      <nav class="header-nav" aria-label="顶部导航">
        <RouterLink v-for="menu in topMenus" :key="menu.id" :to="menu.path"
          :class="{ active: activeTopMenu?.id === menu.id }">
          {{ menu.name }}
        </RouterLink>
      </nav>

      <div class="header-user">{{ username }}</div>
    </header>
    <!-- 手机端菜单开关 -->
    <div v-if="mobileMenuOpen" class="mobile-menu-mask" @click="closeMobileMenu"></div>

    <div class="layout-body" :class="{ 'home-layout': route.path === '/' }">
      <aside id="mobile-sidebar" class="layout-sidebar" :class="{ 'mobile-open': mobileMenuOpen }">
        <!-- 手机端侧边导航 -->
        <nav class="mobile-top-nav" aria-label="手机端主导航">
          <RouterLink v-for="menu in topMenus" :key="menu.id" :to="menu.path"
            :class="{ active: activeTopMenu?.id === menu.id }" @click="closeMobileMenu">
            {{ menu.name }}
          </RouterLink>
        </nav>
        <!-- 电脑端侧边导航 -->
        <!-- <nav aria-label="侧边导航">
          <RouterLink v-for="menu in sideMenus" :key="menu.id" :to="menu.path" class="side-menu-item"
            :class="{ active: route.path === menu.path }" @click="closeMobileMenu">
            <i v-if="menu.icon" :class="menu.icon" aria-hidden="true"></i>
            <span>{{ menu.name }}</span>
          </RouterLink>
        </nav> -->
        <nav aria-label="侧边导航">
          <div v-for="menu in sideMenus" :key="menu.id" class="side-menu-group">
            <RouterLink :to="menu.path" class="side-menu-item" :class="{
              active:
                route.path === menu.path ||
                navigationStore.getChildMenus(menu.id).some(
                  (child) => child.path === route.path,
                ),
            }" @click="closeMobileMenu">
              <i v-if="menu.icon" :class="menu.icon" aria-hidden="true"></i>
              <span>{{ menu.name }}</span>
            </RouterLink>

            <div v-if="navigationStore.getChildMenus(menu.id).length" class="side-submenu">
              <RouterLink v-for="child in navigationStore.getChildMenus(menu.id)" :key="child.id" :to="child.path"
                class="side-submenu-item" :class="{ active: route.path === child.path }" @click="closeMobileMenu">
                {{ child.name }}
              </RouterLink>
            </div>
          </div>
        </nav>
      </aside>

      <main class="layout-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>
<style scoped lang="scss" src="./main-layout.scss"></style>