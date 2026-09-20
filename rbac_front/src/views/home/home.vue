<script src="./home.js"></script>

<template>
  <main class="home-page">
    <section class="welcome-card">
      <div class="card-title">
        <i class="bi bi-shield-lock" aria-hidden="true"></i>
        <span>RBAC 权限管理系统</span>
      </div>

      <p>
        当前用户：
        <strong>{{ user?.username || '未知用户' }}</strong>
      </p>

      <p v-if="user?.role">
        当前角色：
        <strong>{{ user.role.name }}</strong>
      </p>

      <p v-else-if="user?.is_root">
        当前身份：超级管理员
      </p>

      <button
        type="button"
        class="logout-button"
        :disabled="logoutLoading"
        @click="handleLogout"
      >
        <i class="bi bi-box-arrow-right" aria-hidden="true"></i>
        {{ logoutLoading ? '退出中...' : '退出登录' }}
      </button>
    </section>
  </main>
</template>

<style scoped lang="scss" src="./home.scss"></style>