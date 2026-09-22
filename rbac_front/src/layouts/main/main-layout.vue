<script src="./main-layout.js"></script>

<template>
  <div class="main-layout">
    <!-- ==================== 顶部导航栏 ==================== -->
    <header class="layout-header">
      <!-- 手机端：打开或关闭侧边抽屉 -->
      <button
        type="button"
        class="mobile-menu-button"
        :aria-label="mobileMenuOpen ? '关闭侧边菜单' : '打开侧边菜单'"
        aria-controls="mobile-sidebar"
        :aria-expanded="mobileMenuOpen"
        @click="toggleMobileMenu"
      >
        <i class="bi bi-list" aria-hidden="true"></i>
      </button>

      <!-- 手机端顶部 Logo；电脑端 Logo 显示在侧边栏 -->
      <div class="header-brand">
        <span class="logo-dot" aria-hidden="true"></span>
        <span>RBAC</span>
      </div>

      <!-- 电脑端顶部主导航：固定首页 + 接口菜单 -->
      <nav class="header-nav" aria-label="顶部导航">
        <RouterLink
          v-for="menu in topMenus"
          :key="menu.id"
          :to="menu.path"
          :class="{ active: activeTopMenu?.id === menu.id }"
        >
          {{ menu.name }}
        </RouterLink>
      </nav>

      <div class="header-user">{{ username }}</div>
    </header>

    <!-- ==================== 手机端抽屉遮罩 ==================== -->
    <div
      v-if="mobileMenuOpen"
      class="mobile-menu-mask"
      @click="closeMobileMenu"
    ></div>

    <!-- ==================== 侧边栏与页面内容 ==================== -->
    <div class="layout-body">
      <aside
        id="mobile-sidebar"
        class="layout-sidebar"
        :class="{ 'mobile-open': mobileMenuOpen }"
      >
        <!-- 电脑端侧边栏 Logo -->
        <div class="header-brand sidebar-brand">
          <span class="logo-dot" aria-hidden="true"></span>
          <span>RBAC</span>
        </div>

        <!-- 手机端抽屉顶部：主导航 -->
        <nav class="mobile-top-nav" aria-label="手机端主导航">
          <RouterLink
            v-for="menu in topMenus"
            :key="menu.id"
            :to="menu.path"
            :class="{ active: activeTopMenu?.id === menu.id }"
            @click="closeMobileMenu"
          >
            {{ menu.name }}
          </RouterLink>
        </nav>

        <!-- 当前主导航下的侧边菜单；首页使用固定入口 -->
        <nav aria-label="侧边导航">
          <RouterLink
            v-for="menu in sideMenus"
            :key="menu.id"
            :to="menu.path"
            class="side-menu-item"
            :class="{
              active: route.path === '/'
                ? menu.path === `/${route.hash || '#overview'}`
                : route.path === menu.path
            }"
            @click="closeMobileMenu"
          >
            <i v-if="menu.icon" :class="menu.icon" aria-hidden="true"></i>
            <span>{{ menu.name }}</span>
          </RouterLink>
        </nav>

        <!-- 预留：以后启用三级菜单时，可恢复下面的分组结构。
             启用时还需从 main-layout.js 的 setup() 返回 navigationStore。 -->
        <!--
        <nav aria-label="侧边导航">
          <div v-for="menu in sideMenus" :key="menu.id" class="side-menu-group">
            <RouterLink
              :to="menu.path"
              class="side-menu-item"
              :class="{
                active:
                  route.path === menu.path ||
                  navigationStore.getChildMenus(menu.id).some(
                    (child) => child.path === route.path,
                  ),
              }"
              @click="closeMobileMenu"
            >
              <i v-if="menu.icon" :class="menu.icon" aria-hidden="true"></i>
              <span>{{ menu.name }}</span>
            </RouterLink>

            <div
              v-if="navigationStore.getChildMenus(menu.id).length"
              class="side-submenu"
            >
              <RouterLink
                v-for="child in navigationStore.getChildMenus(menu.id)"
                :key="child.id"
                :to="child.path"
                class="side-submenu-item"
                :class="{ active: route.path === child.path }"
                @click="closeMobileMenu"
              >
                {{ child.name }}
              </RouterLink>
            </div>
          </div>
        </nav>
        -->
      </aside>

      <!-- ==================== 当前路由页面 ==================== -->
      <main class="layout-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style scoped lang="scss" src="./main-layout.scss"></style>