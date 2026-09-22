<script src="./home.js"></script>

<template>
  <main class="home-page">
    <div id="overview" class="page-heading">
      <p class="page-label">OVERVIEW</p>
      <h1>欢迎回来，{{ user?.username || '用户' }}</h1>
      <p>这里是你的账户概览。</p>
    </div>

    <section id="account" class="account-card" aria-labelledby="account-title">
      <div class="card-heading">
        <i class="bi bi-person-circle" aria-hidden="true"></i>
        <div>
          <h2 id="account-title">账户信息</h2>
          <p>当前登录账户的基本资料</p>
        </div>
      </div>

      <dl class="account-details">
        <div>
          <dt>用户名</dt>
          <dd>{{ user?.username || '未知用户' }}</dd>
        </div>

        <div>
          <dt>当前身份</dt>
          <dd v-if="user?.is_root">超级管理员</dd>
          <dd v-else-if="user?.role">{{ user.role.name }}</dd>
          <dd v-else>未分配角色</dd>
        </div>

        <div v-if="user?.email">
          <dt>邮箱</dt>
          <dd>{{ user.email }}</dd>
        </div>
      </dl>

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