<!-- ==================== 首页业务逻辑 ==================== -->
<script src="./home.js"></script>

<template>
  <div class="home-page">
    <!-- ==================== 页面标题 ==================== -->
    <header class="page-heading">
      <h1>首页</h1>
      <p>欢迎使用 BP Workbench</p>
    </header>

    <!-- ==================== 首页卡片区域 ==================== -->
    <section
      class="card-grid"
      aria-label="首页工作台"
    >
      <!-- ==================== 卡片 1 ==================== -->
      <article class="dashboard-card card-1">
        <header class="card-header">
          <h2 class="card-title">
            卡片 1
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 1 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-bar-chart"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              可替换为统计数据、图表或其他内容
            </small>
          </div>
        </div>
      </article>

      <!-- ==================== 卡片 2 ==================== -->
      <article class="dashboard-card card-2">
        <header class="card-header">
          <h2 class="card-title">
            卡片 2
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 2 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-clock"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              可替换为统计数据、图表或其他内容
            </small>
          </div>
        </div>
      </article>

      <!-- ==================== 卡片 3 ==================== -->
      <article class="dashboard-card card-3">
        <header class="card-header">
          <h2 class="card-title">
            卡片 3
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 3 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-window"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              在这里添加自定义内容
            </small>
          </div>
        </div>
      </article>

      <!-- ==================== 卡片 4 ==================== -->
      <article class="dashboard-card card-4">
        <header class="card-header">
          <h2 class="card-title">
            卡片 4
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 4 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-people"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              在这里添加自定义内容
            </small>
          </div>
        </div>
      </article>

      <!-- ==================== 卡片 5 ==================== -->
      <article class="dashboard-card card-5">
        <header class="card-header">
          <h2 class="card-title">
            卡片 5
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 5 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-person"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              在这里添加自定义内容
            </small>
          </div>
        </div>
      </article>

      <!-- ==================== 卡片 6 ==================== -->
      <article class="dashboard-card card-6">
        <header class="card-header">
          <h2 class="card-title">
            卡片 6
          </h2>

          <button
            class="card-action"
            type="button"
            aria-label="卡片 6 更多操作"
          >
            <i
              class="bi bi-three-dots"
              aria-hidden="true"
            ></i>
          </button>
        </header>

        <div class="card-body">
          <div class="card-placeholder">
            <div
              class="card-placeholder-icon"
              aria-hidden="true"
            >
              <i class="bi bi-bar-chart-line"></i>
            </div>

            <span>卡片内容区域</span>

            <small>
              可替换为表格、日志或其他较宽的内容
            </small>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<!-- ==================== 首页样式 ==================== -->
<style
  scoped
  lang="scss"
  src="./home.scss"
></style>