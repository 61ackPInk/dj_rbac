<!-- ==================== 后台布局业务逻辑 ==================== -->
<script src="./main-layout.js"></script>

<template>
  <div
    class="app-layout"
    :class="{
      'is-collapsed': sidebarCollapsed,
      'is-mobile-open': mobileSidebarOpen,
    }"
  >
    <!-- ==================== 左侧导航栏 ==================== -->
    <aside
      id="main-sidebar"
      class="layout-sidebar"
    >
      <!-- 侧边栏品牌 -->
      <header class="sidebar-header">
        <RouterLink
          class="sidebar-brand"
          to="/"
          aria-label="返回首页"
          @click="closeMobileSidebar"
        >
          <span
            class="brand-logo"
            aria-hidden="true"
          >
            <i class="bi bi-grid"></i>
          </span>

          <span class="brand-name">
            BP Workbench
          </span>
        </RouterLink>
      </header>

      <!-- ==================== 侧边栏菜单 ==================== -->
      <nav
        class="sidebar-content"
        aria-label="后台主导航"
      >
        <!-- 固定首页入口 -->
        <section class="menu-group">
          <p class="menu-title">
            工作台
          </p>

          <RouterLink
            class="menu-item"
            :class="{ 'is-active': route.path === '/' }"
            to="/"
            title="首页"
            @click="closeMobileSidebar"
          >
            <span
              class="menu-icon"
              aria-hidden="true"
            >
              <i class="bi bi-grid"></i>
            </span>

            <span class="menu-text">
              首页
            </span>
          </RouterLink>
        </section>

        <!-- 后端返回的动态菜单分组 -->
        <section
          v-for="group in menuGroups"
          :key="group.id"
          class="menu-group"
        >
          <!-- 根页面作为菜单分组标题 -->
          <p class="menu-title">
            {{ group.name }}
          </p>

          <!-- 根页面下的子页面 -->
          <RouterLink
            v-for="menu in group.children"
            :key="menu.id"
            class="menu-item"
            :class="{
              'is-active': isMenuActive(menu.path),
            }"
            :to="menu.path"
            :title="menu.name"
            @click="closeMobileSidebar"
          >
            <span
              class="menu-icon"
              aria-hidden="true"
            >
              <i
                class="bi"
                :class="menu.icon || 'bi-circle'"
              ></i>
            </span>

            <span class="menu-text">
              {{ menu.name }}
            </span>
          </RouterLink>
        </section>
      </nav>

      <!-- ==================== 侧边栏底部 ==================== -->
      <footer class="sidebar-footer">
        <div class="system-status">
          <span
            class="status-dot"
            aria-hidden="true"
          ></span>

          <span class="status-text">
            系统运行正常
          </span>
        </div>
      </footer>
    </aside>

    <!-- ==================== 手机端侧边栏遮罩 ==================== -->
    <button
      v-if="mobileSidebarOpen"
      class="mobile-overlay"
      type="button"
      aria-label="关闭侧边栏"
      @click="closeMobileSidebar"
    ></button>

    <!-- ==================== 后台主体 ==================== -->
    <div class="layout-main">
      <!-- ==================== 顶部栏 ==================== -->
      <header class="layout-topbar">
        <!-- 顶部栏左侧 -->
        <div class="topbar-left">
          <!-- 侧边栏切换按钮 -->
          <button
            class="sidebar-toggle"
            type="button"
            aria-controls="main-sidebar"
            :aria-expanded="
              mobileSidebarOpen || !sidebarCollapsed
            "
            :aria-label="
              mobileSidebarOpen
                ? '关闭侧边栏'
                : '切换侧边栏'
            "
            @click="toggleSidebar"
          >
            <i
              class="bi bi-list"
              aria-hidden="true"
            ></i>
          </button>

          <!-- 页面面包屑 -->
          <nav
            class="breadcrumb"
            aria-label="面包屑导航"
          >
            <span>BP Workbench</span>

            <template v-if="currentMenuGroup">
              <i
                class="bi bi-chevron-right breadcrumb-separator"
                aria-hidden="true"
              ></i>

              <span>
                {{ currentMenuGroup.name }}
              </span>
            </template>

            <i
              class="bi bi-chevron-right breadcrumb-separator"
              aria-hidden="true"
            ></i>

            <strong class="mobile-page-name">
              {{ currentPageName }}
            </strong>
          </nav>
        </div>

        <!-- ==================== 右上角用户菜单 ==================== -->
        <div
          class="user-menu"
          @click.stop="stopUserMenuPropagation"
        >
          <!-- 用户菜单触发按钮 -->
          <button
            class="user-trigger"
            :class="{ 'is-open': userMenuOpen }"
            type="button"
            aria-haspopup="true"
            :aria-expanded="userMenuOpen"
            @click="toggleUserMenu"
          >
            <!-- 用户头像 -->
            <span class="topbar-avatar">
              {{ userInitial }}
            </span>

            <!-- 用户信息 -->
            <span class="topbar-user-info">
              <span class="topbar-user-name">
                {{ userDisplayName }}
              </span>

              <span class="topbar-user-role">
                {{ userRoleName }}
              </span>
            </span>

            <!-- 展开箭头 -->
            <i
              class="bi bi-chevron-down user-arrow"
              aria-hidden="true"
            ></i>
          </button>

          <!-- 用户下拉菜单 -->
          <Transition name="user-dropdown">
            <div
              v-if="userMenuOpen"
              class="user-dropdown"
              role="menu"
            >
              <!-- 个人中心 -->
              <button
                class="dropdown-item"
                type="button"
                role="menuitem"
                @click="showUnavailable('个人中心')"
              >
                <i
                  class="bi bi-person"
                  aria-hidden="true"
                ></i>

                <span>个人中心</span>
              </button>

              <div
                class="dropdown-divider"
                aria-hidden="true"
              ></div>

              <!-- 退出登录 -->
              <button
                class="dropdown-item logout"
                type="button"
                role="menuitem"
                :disabled="logoutLoading"
                @click="handleLogout"
              >
                <i
                  class="bi bi-box-arrow-right"
                  aria-hidden="true"
                ></i>

                <span>
                  {{
                    logoutLoading
                      ? '正在退出...'
                      : '退出登录'
                  }}
                </span>
              </button>
            </div>
          </Transition>
        </div>
      </header>

      <!-- ==================== 当前路由页面 ==================== -->
      <main class="layout-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<!-- ==================== 后台布局样式 ==================== -->
<style
  scoped
  lang="scss"
  src="./main-layout.scss"
></style>




<!-- 
页面结构
app-layout
├── layout-sidebar
│   ├── sidebar-header
│   ├── sidebar-content
│   │   ├── 固定首页
│   │   └── 后端动态菜单
│   └── sidebar-footer
├── mobile-overlay
└── layout-main
    ├── layout-topbar
    │   ├── 面包屑
    │   └── 用户菜单
    └── layout-content
        └── RouterView
-->