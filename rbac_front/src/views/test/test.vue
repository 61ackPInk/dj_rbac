<template>
  <div class="admin-layout">
    <!-- 移动端遮罩，侧边栏打开时显示 -->
    <div
      v-if="mobileSidebarOpen"
      class="layout-mask"
      @click="closeMobileSidebar"
    ></div>

    <!-- 左侧侧边栏 -->
    <aside
      class="layout-sidebar"
      :class="[
        { 'sidebar-collapsed': sidebarCollapsed },
        { 'sidebar-mobile-show': mobileSidebarOpen }
      ]"
    >
      <!-- Logo/系统名称区域 -->
      <div class="sidebar-logo">
        <i class="bi bi-shield-lock"></i>
        <span v-if="!sidebarCollapsed">RBAC权限管理系统</span>
      </div>

      <!-- 菜单列表 -->
      <nav class="sidebar-menu">
        <div
          v-for="menu in menuList"
          key="menu.path"
          class="menu-item"
          :class="{ 'menu-active': activeMenu === menu.path }"
          @click="handleMenuClick(menu)"
        >
          <i :class="menu.icon"></i>
          <span v-if="!sidebarCollapsed">{{ menu.label }}</span>
        </div>
      </nav>
    </aside>

    <!-- 主容器区域 -->
    <div class="layout-main">
      <!-- 顶部导航栏 -->
      <header class="layout-header">
        <div class="header-left">
          <!-- 桌面端：折叠侧边栏按钮；移动端：打开抽屉按钮 -->
          <button
            class="btn-toggle-sidebar"
            @click="toggleSidebar"
          >
            <i class="bi bi-list"></i>
          </button>
          <h2 class="page-title">{{ currentPageTitle }}</h2>
        </div>

        <div class="header-right">
          <!-- 主题切换按钮 -->
          <button class="btn-theme" @click="toggleTheme">
            <i :class="isDark ? 'bi bi-sun' : 'bi bi-moon-stars'"></i>
          </button>

          <!-- 用户下拉菜单 -->
          <div class="user-dropdown" @click="dropdownVisible = !dropdownVisible">
            <div class="user-info">
              <div class="user-avatar">
                <i class="bi bi-person-circle"></i>
              </div>
              <div class="user-text">
                <div class="username">管理员</div>
                <div class="user-role">超级管理员</div>
              </div>
              <i class="bi bi-chevron-down dropdown-arrow"></i>
            </div>

            <!-- 用户下拉浮层 -->
            <div v-if="dropdownVisible" class="user-dropdown-menu">
              <div class="dropdown-item" @click.stop="dropdownVisible = false">
                <i class="bi bi-person"></i>
                <span>个人信息</span>
              </div>
              <div class="dropdown-item" @click.stop="dropdownVisible = false">
                <i class="bi bi-key"></i>
                <span>修改密码</span>
              </div>
              <div class="dropdown-divider"></div>
              <div class="dropdown-item danger" @click.stop="handleLogout">
                <i class="bi bi-box-arrow-right"></i>
                <span>退出登录</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- 页面内容区域，放置router-view -->
      <main class="layout-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 侧边栏状态：桌面端折叠
const sidebarCollapsed = ref(false)
// 移动端侧边抽屉开关
const mobileSidebarOpen = ref(false)
// 用户下拉菜单
const dropdownVisible = ref(false)
// 主题状态，仅本地切换标记，不实现完整主题逻辑
const isDark = ref(false)

// 静态菜单数据，RBAC基础菜单
const menuList = ref([
  { label: '首页', path: '/dashboard', icon: 'bi bi-house-door' },
  { label: '用户管理', path: '/system/user', icon: 'bi bi-people' },
  { label: '角色管理', path: '/system/role', icon: 'bi bi-person-badge' },
  { label: '页面管理', path: '/system/page', icon: 'bi bi-file-earmark-text' },
])

// 当前激活菜单
const activeMenu = computed(() => route.path)
// 当前页面标题
const currentPageTitle = computed(() => {
  const matched = menuList.value.find(item => item.path === route.path)
  return matched ? matched.label : 'RBAC管理后台'
})

// 判断是否移动端
const isMobile = ref(false)
const checkDevice = () => {
  isMobile.value = window.innerWidth < 768
  // 窗口变大自动关闭移动端抽屉
  if (!isMobile.value) {
    mobileSidebarOpen.value = false
  }
}

onMounted(() => {
  checkDevice()
  window.addEventListener('resize', checkDevice)
})

// 侧边栏切换逻辑：区分桌面/移动端
const toggleSidebar = () => {
  if (isMobile.value) {
    mobileSidebarOpen.value = !mobileSidebarOpen.value
  } else {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}

// 关闭移动端侧边抽屉
const closeMobileSidebar = () => {
  mobileSidebarOpen.value = false
}

// 菜单点击
const handleMenuClick = () => {
  // 移动端点击菜单后关闭抽屉
  if (isMobile.value) {
    mobileSidebarOpen.value = false
  }
  dropdownVisible.value = false
}

// 主题切换，仅本地状态，不做实际样式变更
const toggleTheme = () => {
  isDark.value = !isDark.value
}

// 退出登录，仅占位，不调用接口
const handleLogout = () => {
  alert('执行退出登录（仅模拟）')
  dropdownVisible.value = false
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background-color: var(--app-page-bg-primary);
}

// 移动端遮罩
.layout-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.45);
  z-index: 99;
}

// -------------------侧边栏样式-------------------
.layout-sidebar {
  width: 240px;
  flex-shrink: 0;
  height: 100vh;
  background-color: var(--app-page-bg-minor);
  border-right: 1px solid var(--app-border);
  transition: width 0.28s ease;
  overflow: hidden;
  z-index: 100;
  display: flex;
  flex-direction: column;

  &.sidebar-collapsed {
    width: 64px;
  }

  // 移动端抽屉模式
  @media (max-width: 767px) {
    position: fixed;
    left: -240px;
    top: 0;
    width: 240px;

    &.sidebar-mobile-show {
      left: 0;
    }

    &.sidebar-collapsed {
      width: 240px;
    }
  }
}

.sidebar-logo {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  font-size: 16px;
  font-weight: 600;
  color: var(--app-text-title);
  border-bottom: 1px solid var(--app-border-line);
  flex-shrink: 0;

  i {
    font-size: 22px;
    flex-shrink: 0;
  }
}

.sidebar-menu {
  flex: 1;
  padding: 12px 0;
  overflow-y: auto;

  .menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    height: 44px;
    padding: 0 16px;
    cursor: pointer;
    color: var(--app-text-minor);
    transition: background-color 0.2s, color 0.2s;
    white-space: nowrap;

    i {
      font-size: 18px;
      flex-shrink: 0;
    }

    &:hover {
      background-color: var(--app-card);
      color: var(--app-text-hover);
    }

    &.menu-active {
      background-color: var(--app-card);
      color: var(--app-text-title);
      border-right: 3px solid var(--app-btn);
    }
  }
}

// ----------------主内容容器----------------
.layout-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

// ----------------顶部头部栏----------------
.layout-header {
  height: 60px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background-color: var(--app-page-bg-minor);
  border-bottom: 1px solid var(--app-border);

  .header-left {
    display: flex;
    align-items: center;
    gap: 14px;

    .btn-toggle-sidebar {
      width: 36px;
      height: 36px;
      border-radius: var(--app-radius-btn);
      border: 1px solid var(--app-border);
      background-color: var(--app-card);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--app-text-title);

      &:hover {
        background-color: var(--app-btn-hover);
        color: var(--app-btn-text-hover);
      }
    }

    .page-title {
      margin: 0;
      font-size: 17px;
      font-weight: 500;
      color: var(--app-text-title);
    }
  }

  .header-right {
    display: flex;
    align-items: center;
    gap: 16px;

    .btn-theme {
      width: 36px;
      height: 36px;
      border-radius: var(--app-radius-btn);
      border: 1px solid var(--app-border);
      background-color: var(--app-card);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--app-text-title);

      &:hover {
        background-color: var(--app-btn-hover);
        color: var(--app-btn-text-hover);
      }
    }
  }
}

// 用户下拉菜单
.user-dropdown {
  position: relative;
  cursor: pointer;

  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;

    .user-avatar {
      font-size: 28px;
      color: var(--app-text-title);
    }

    .user-text {
      .username {
        font-size: 14px;
        color: var(--app-text-title);
        line-height: 1.3;
      }
      .user-role {
        font-size: 12px;
        color: var(--app-text-description);
        line-height: 1.3;
      }
    }
    .dropdown-arrow {
      font-size: 13px;
      color: var(--app-text-description);
    }
  }

  .user-dropdown-menu {
    position: absolute;
    top: calc(100% + 6px);
    right: 0;
    min-width: 160px;
    background-color: var(--app-card);
    border: 1px solid var(--app-border);
    border-radius: var(--app-radius-card);
    box-shadow: var(--app-card-shadow);
    overflow: hidden;
    z-index: 102;

    .dropdown-item {
      display: flex;
      align-items: center;
      gap: 8px;
      height: 40px;
      padding: 0 14px;
      font-size: 14px;
      color: var(--app-text-title);
      transition: background 0.2s;

      i {
        font-size: 16px;
        color: var(--app-text-minor);
      }

      &:hover {
        background-color: var(--app-page-bg-primary);
      }

      &.danger {
        color: #dd4444;
        i {
          color: #dd4444;
        }
      }
    }

    .dropdown-divider {
      height: 1px;
      background-color: var(--app-border-line);
      margin: 4px 0;
    }
  }
}

// ----------------页面内容区----------------
.layout-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: var(--app-page-bg-primary);
}

// 移动端适配调整
@media (max-width: 767px) {
  .layout-header {
    padding: 0 12px;
  }
  .layout-content {
    padding: 14px;
  }
}
</style>
