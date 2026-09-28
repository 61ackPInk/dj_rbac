<!-- ==================== 角色管理业务逻辑 ==================== -->

<script src="./roles.js"></script>

<template>
  <div class="roles-page">
    <!-- ==================== 页面标题 ==================== -->

    <header class="page-heading">
      <div>
        <h1>角色管理</h1>
        <p>
          管理系统角色、角色权重和启用状态。
        </p>
      </div>
    </header>

    <!-- ==================== 页面开发提示 ==================== -->

    <section class="roles-placeholder">
      <i
        class="bi bi-person-badge"
        aria-hidden="true"
      ></i>

      <strong>角色管理</strong>

      <span>
        页面路由已经建立，下一步接入角色数据。
      </span>
    </section>
  </div>
</template>

<!-- ==================== 角色管理页面样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./roles.scss"
></style>

<!-- ==================== 角色弹出层业务样式 ==================== -->

<!--
  AppModal 会将弹出层传送到 body 下，
  因此角色弹出层内容使用单独的非 scoped 样式文件。
-->
<style
  lang="scss"
  src="./roles-modal.scss"
></style>