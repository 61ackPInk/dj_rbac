<!-- ==================== 页面管理业务逻辑 ==================== -->

<script src="./pages.js"></script>

<template>
  <div class="pages-page">
    <!-- ==================== 页面标题 ==================== -->

    <header class="page-heading">
      <div>
        <h1>页面管理</h1>

        <p>
          管理系统页面、导航图标、访问角色和启用状态。
        </p>
      </div>
    </header>

    <!-- ==================== 页面开发提示 ==================== -->

    <section class="pages-placeholder">
      <i
        class="bi bi-window"
        aria-hidden="true"
      ></i>

      <strong>页面管理</strong>

      <span>
        页面路由已经建立，下一步接入页面数据。
      </span>
    </section>
  </div>
</template>

<!-- ==================== 页面管理样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./pages.scss"
></style>

<!-- ==================== 页面弹出层样式 ==================== -->

<style
  lang="scss"
  src="./pages-modal.scss"
></style>