<!-- ==================== 系统概览业务逻辑 ==================== -->
<script src="./dashboard.js"></script>

<template>
  <div class="system-dashboard">
    <!-- ==================== 页面标题 ==================== -->
    <header class="page-heading">
      <div class="page-title-group">
        <h1>系统概览</h1>
        <p>查看当前系统的用户、角色与页面配置情况。</p>
      </div>

      <span class="update-time">数据更新时间：{{ formatUpdatedAt }}</span>
    </header>

    <!-- ==================== 加载状态 ==================== -->
    <section v-if="loading" class="dashboard-state" aria-live="polite">
      <i class="bi bi-arrow-clockwise state-loading" aria-hidden="true"></i>
      <strong>正在加载系统概览</strong>
      <span>请稍候...</span>
    </section>

    <!-- ==================== 错误状态 ==================== -->
    <section v-else-if="errorMessage" class="dashboard-state error" role="alert">
      <i class="bi bi-exclamation-circle" aria-hidden="true"></i>
      <strong>系统概览加载失败</strong>
      <span>{{ errorMessage }}</span>
      <button class="retry-button" type="button" @click="loadOverview">重新加载</button>
    </section>

    <template v-else>
      <!-- ==================== 核心数据 ==================== -->
      <section class="overview-grid" aria-label="系统核心数据">
        <article class="overview-card">
          <div class="overview-header">
            <div><div class="overview-label">用户总数</div><div class="overview-en">USERS</div></div>
            <div class="overview-icon" aria-hidden="true"><i class="bi bi-people"></i></div>
          </div>
          <div class="overview-number">{{ formatNumber(overview.users.total) }}</div>
          <div class="overview-footer">
            <span class="overview-description">启用 {{ formatNumber(overview.users.active) }} 位用户</span>
            <button class="overview-link" type="button" @click="navigateTo('system-users')">
              <span>查看用户</span><i class="bi bi-chevron-right" aria-hidden="true"></i>
            </button>
          </div>
        </article>

        <article class="overview-card green">
          <div class="overview-header">
            <div><div class="overview-label">角色总数</div><div class="overview-en">ROLES</div></div>
            <div class="overview-icon" aria-hidden="true"><i class="bi bi-person-badge"></i></div>
          </div>
          <div class="overview-number">{{ formatNumber(overview.roles.total) }}</div>
          <div class="overview-footer">
            <span class="overview-description">启用 {{ formatNumber(overview.roles.active) }} 个角色</span>
            <button class="overview-link" type="button" @click="navigateTo('system-roles')">
              <span>查看角色</span><i class="bi bi-chevron-right" aria-hidden="true"></i>
            </button>
          </div>
        </article>

        <article class="overview-card orange">
          <div class="overview-header">
            <div><div class="overview-label">页面总数</div><div class="overview-en">PAGES</div></div>
            <div class="overview-icon" aria-hidden="true"><i class="bi bi-layout-text-window"></i></div>
          </div>
          <div class="overview-number">{{ formatNumber(overview.pages.total) }}</div>
          <div class="overview-footer">
            <span class="overview-description">启用 {{ formatNumber(overview.pages.active) }} 个页面</span>
            <button class="overview-link" type="button" @click="navigateTo('system-pages')">
              <span>查看页面</span><i class="bi bi-chevron-right" aria-hidden="true"></i>
            </button>
          </div>
        </article>
      </section>

      <!-- ==================== 中部数据区域 ==================== -->
      <section class="middle-grid">
        <article class="panel">
          <header class="panel-header">
            <div class="panel-title"><h2>用户状态</h2><p>当前系统用户状态分布</p></div>
            <button class="panel-action" type="button" @click="navigateTo('system-users')">用户管理</button>
          </header>

          <div class="user-status-content">
            <div class="donut-wrapper">
              <div class="donut" :style="donutStyle">
                <div class="donut-center"><strong>{{ formatNumber(overview.users.total) }}</strong><span>全部用户</span></div>
              </div>
            </div>

            <div class="status-list">
              <div v-for="status in userStatuses" :key="status.key" class="status-item">
                <div class="status-item-header">
                  <span class="status-name"><i class="legend-dot" :class="status.colorClass" aria-hidden="true"></i>{{ status.label }}</span>
                  <span class="status-value">{{ formatNumber(status.value) }}</span>
                </div>
                <div class="progress">
                  <div class="progress-bar" :class="status.colorClass" :style="{ width: `${getStatusPercentage(status.value)}%` }"></div>
                </div>
              </div>
            </div>
          </div>
        </article>

        <article class="panel">
          <header class="panel-header">
            <div class="panel-title"><h2>角色分布</h2><p>各角色当前用户数量</p></div>
            <button class="panel-action" type="button" @click="navigateTo('system-roles')">全部角色</button>
          </header>

          <div v-if="roleDistribution.length" class="role-list">
            <div v-for="role in roleDistribution" :key="role.id" class="role-item">
              <span class="role-icon" :class="{ muted: role.unassigned }">
                <i :class="role.unassigned ? 'bi bi-person-dash' : 'bi bi-person-badge'"></i>
              </span>
              <div class="role-info"><strong>{{ role.name }}</strong><span>{{ role.code }}</span></div>
              <span class="role-count">{{ formatNumber(role.userCount) }} 人</span>
            </div>
          </div>
          <div v-else class="panel-empty"><i class="bi bi-person-badge" aria-hidden="true"></i><span>暂无角色分布数据</span></div>
        </article>
      </section>

      <!-- ==================== 底部数据区域 ==================== -->
      <section class="bottom-grid">
        <article class="panel">
          <header class="panel-header">
            <div class="panel-title"><h2>页面数据</h2><p>系统页面配置统计</p></div>
            <button class="panel-action" type="button" @click="navigateTo('system-pages')">页面管理</button>
          </header>

          <div class="page-list">
            <div class="page-item"><div class="page-icon"><i class="bi bi-window"></i></div><div class="page-info"><strong>全部页面</strong><span>系统页面总数</span></div><span class="page-number">{{ formatNumber(overview.pages.total) }}</span></div>
            <div class="page-item"><div class="page-icon"><i class="bi bi-check-lg"></i></div><div class="page-info"><strong>启用页面</strong><span>当前可以正常访问</span></div><span class="page-number">{{ formatNumber(overview.pages.active) }}</span></div>
            <div class="page-item"><div class="page-icon"><i class="bi bi-list-ul"></i></div><div class="page-info"><strong>一级页面</strong><span>顶级菜单页面</span></div><span class="page-number">{{ formatNumber(overview.pages.top_level) }}</span></div>
            <div class="page-item"><div class="page-icon"><i class="bi bi-exclamation-circle"></i></div><div class="page-info"><strong>禁用页面</strong><span>当前禁止访问</span></div><span class="page-number">{{ formatNumber(overview.pages.disabled) }}</span></div>
          </div>
        </article>

        <article class="panel">
          <header class="panel-header">
            <div class="panel-title"><h2>最近新增用户</h2><p>最新加入系统的用户</p></div>
            <button class="panel-action" type="button" @click="navigateTo('system-users')">全部用户</button>
          </header>

          <div v-if="overview.recent_users.length" class="table-wrapper">
            <table class="data-table">
              <thead><tr><th>用户</th><th>角色</th><th>状态</th></tr></thead>
              <tbody>
                <tr v-for="user in overview.recent_users" :key="user.id">
                  <td><div class="table-user"><span class="table-avatar">{{ getUserInitial(user) }}</span><strong>{{ user.username }}</strong></div></td>
                  <td>{{ user.role || '未分配角色' }}</td>
                  <td><span class="tag" :class="user.status === '启用' ? 'enabled' : 'disabled'">{{ user.status || '未知' }}</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="panel-empty"><i class="bi bi-person-plus" aria-hidden="true"></i><span>暂无最近新增用户</span></div>
        </article>
      </section>
    </template>
  </div>
</template>

<!-- ==================== 系统概览样式 ==================== -->
<style scoped lang="scss" src="./dashboard.scss"></style>
