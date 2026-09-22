<script src="./dashboard.js"></script>

<template>
  <section class="system-dashboard">
    <header class="dashboard-heading">
      <p v-if="parentPage && currentPage">
        {{ parentPage.name }} / {{ currentPage.name }}
      </p>

      <h1>{{ currentPage?.name || '加载中...' }}</h1>

      <p>这里将展示系统管理相关的真实统计信息。</p>
    </header>
  </section>
</template>