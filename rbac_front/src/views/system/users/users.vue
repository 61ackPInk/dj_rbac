<script src="./users.js"></script>

<template>
  <section class="users-page">
    <!-- ==================== 页面标题 ==================== -->
    <header class="users-heading">
      <p v-if="parentPage && currentPage" class="users-breadcrumb">
        {{ parentPage.name }} / {{ currentPage.name }}
      </p>
      <h1>{{ currentPage?.name || '加载中...' }}</h1>
      <p>查看系统账号、角色和启用状态。</p>
    </header>

    <!-- ==================== 真实用户数量 ==================== -->
    <div class="users-summary">
      <div class="summary-card summary-card--total">
        <span>用户总数</span>
        <strong>{{ users.length }}</strong>
      </div>

      <div class="summary-card summary-card--active">
        <span>已启用</span>
        <strong>{{ activeCount }}</strong>
      </div>

      <div class="summary-card summary-card--disabled">
        <span>已停用</span>
        <strong>{{ users.length - activeCount }}</strong>
      </div>
    </div>

    <!-- ==================== 搜索与筛选 ==================== -->
    <div class="users-toolbar">
      <label>
        <span>搜索用户</span>
        <input v-model="keyword" type="search" placeholder="输入用户名或邮箱" />
      </label>

      <label>
        <span>账号状态</span>
        <select v-model="statusFilter">
          <option value="all">全部</option>
          <option value="active">已启用</option>
          <option value="disabled">已停用</option>
        </select>
      </label>

      <button type="button" :disabled="loading" @click="loadUsers">
        {{ loading ? '加载中...' : '刷新列表' }}
      </button>
    </div>

    <!-- ==================== 加载、错误与空状态 ==================== -->
    <p v-if="errorMessage" class="users-notice" role="alert">
      {{ errorMessage }}
    </p>
    <p v-else-if="loading" class="users-notice">正在加载用户...</p>
    <p v-else-if="filteredUsers.length === 0" class="users-notice">
      没有符合条件的用户
    </p>

    <!-- ==================== 用户列表 ==================== -->
    <div v-else class="users-table-wrap">
      <table class="users-table">
        <thead>
          <tr>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>状态</th>
            <th>创建时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email || '—' }}</td>
            <td>
              {{ user.is_root ? '超级管理员' : user.role?.name || '未分配角色' }}
            </td>
            <td>
              <span class="status-badge" :class="user.is_active ? 'is-active' : 'is-disabled'">
                {{ user.is_active ? '已启用' : '已停用' }}
              </span>
            </td>
            <td>{{ formatTime(user.create_time) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
<style scoped lang="scss" src="./users.scss"></style>