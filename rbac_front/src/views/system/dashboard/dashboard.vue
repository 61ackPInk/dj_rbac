<script src="./dashboard.js"></script>

<template>
  <section class="system-dashboard">
    <!-- 页面标题：名称来自后端可见页面数据 -->
    <header class="dashboard-heading">
      <p v-if="parentPage && currentPage" class="dashboard-breadcrumb">
        {{ parentPage.name }} / {{ currentPage.name }}
      </p>

      <h1>{{ currentPage?.name || '加载中...' }}</h1>
      <p class="dashboard-description">
        查看当前系统的用户、角色与页面信息。
      </p>
    </header>

    <!-- 系统统计：接口失败时显示“—”，不显示虚假的 0 -->
    <div class="dashboard-stats">
      <article v-if="isRoot" class="stat-card stat-card--users">
        <i class="bi bi-people stat-icon" aria-hidden="true"></i>
        <p class="stat-label">USERS</p>
        <h2>用户总数</h2>
        <strong>{{ userCount ?? '—' }}</strong>
        <p class="stat-description">
          {{ loading ? '正在读取...' : userCount === null ? '暂时无法获取' : '系统中的全部用户' }}
        </p>
      </article>

      <article class="stat-card stat-card--roles">
        <i class="bi bi-person-badge stat-icon" aria-hidden="true"></i>
        <p class="stat-label">ROLES</p>
        <h2>角色总数</h2>
        <strong>{{ roleCount ?? '—' }}</strong>
        <p class="stat-description">
          {{ loading ? '正在读取...' : roleCount === null ? '暂时无法获取' : '系统中的全部角色' }}
        </p>
      </article>

      <article class="stat-card stat-card--pages">
        <i class="bi bi-grid stat-icon" aria-hidden="true"></i>
        <p class="stat-label">PAGES</p>
        <h2>可见页面</h2>
        <strong>{{ visiblePageCount ?? '—' }}</strong>
        <p class="stat-description">
          当前账号有权查看的页面
        </p>
      </article>
    </div>
  </section>
</template>

<style scoped lang="scss" src="./dashboard.scss"></style>