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

      <span class="update-time">
        数据更新时间：刚刚
      </span>
    </header>

    <!-- ==================== 核心数据 ==================== -->
    <section
      class="overview-grid"
      aria-label="系统核心数据"
    >
      <!-- 用户总数 -->
      <article class="overview-card">
        <div class="overview-header">
          <div>
            <div class="overview-label">
              用户总数
            </div>

            <div class="overview-en">
              USERS
            </div>
          </div>

          <div
            class="overview-icon"
            aria-hidden="true"
          >
            <i class="bi bi-people"></i>
          </div>
        </div>

        <div class="overview-number">
          1,286
        </div>

        <div class="overview-footer">
          <span class="overview-description">
            启用 1,174 位用户
          </span>

          <button
            class="overview-link"
            type="button"
          >
            <span>查看用户</span>

            <i
              class="bi bi-chevron-right"
              aria-hidden="true"
            ></i>
          </button>
        </div>
      </article>

      <!-- 角色总数 -->
      <article class="overview-card green">
        <div class="overview-header">
          <div>
            <div class="overview-label">
              角色总数
            </div>

            <div class="overview-en">
              ROLES
            </div>
          </div>

          <div
            class="overview-icon"
            aria-hidden="true"
          >
            <i class="bi bi-person-badge"></i>
          </div>
        </div>

        <div class="overview-number">
          18
        </div>

        <div class="overview-footer">
          <span class="overview-description">
            启用 16 个角色
          </span>

          <button
            class="overview-link"
            type="button"
          >
            <span>查看角色</span>

            <i
              class="bi bi-chevron-right"
              aria-hidden="true"
            ></i>
          </button>
        </div>
      </article>

      <!-- 页面总数 -->
      <article class="overview-card orange">
        <div class="overview-header">
          <div>
            <div class="overview-label">
              页面总数
            </div>

            <div class="overview-en">
              PAGES
            </div>
          </div>

          <div
            class="overview-icon"
            aria-hidden="true"
          >
            <i class="bi bi-layout-text-window"></i>
          </div>
        </div>

        <div class="overview-number">
          32
        </div>

        <div class="overview-footer">
          <span class="overview-description">
            启用 30 个页面
          </span>

          <button
            class="overview-link"
            type="button"
          >
            <span>查看页面</span>

            <i
              class="bi bi-chevron-right"
              aria-hidden="true"
            ></i>
          </button>
        </div>
      </article>
    </section>

    <!-- ==================== 中部数据区域 ==================== -->
    <section class="middle-grid">
      <!-- ==================== 用户状态 ==================== -->
      <article class="panel">
        <header class="panel-header">
          <div class="panel-title">
            <h2>用户状态</h2>
            <p>当前系统用户状态分布</p>
          </div>

          <button
            class="panel-action"
            type="button"
          >
            用户管理
          </button>
        </header>

        <div class="user-status-content">
          <!-- 环形统计图 -->
          <div class="donut-wrapper">
            <div class="donut">
              <div class="donut-center">
                <strong>1,286</strong>
                <span>全部用户</span>
              </div>
            </div>
          </div>

          <!-- 用户状态列表 -->
          <div class="status-list">
            <!-- 正常用户 -->
            <div class="status-item">
              <div class="status-item-header">
                <span class="status-name">
                  <i
                    class="legend-dot blue"
                    aria-hidden="true"
                  ></i>

                  正常用户
                </span>

                <span class="status-value">
                  938
                </span>
              </div>

              <div class="progress">
                <div
                  class="progress-bar"
                  style="width: 73%"
                ></div>
              </div>
            </div>

            <!-- 新增用户 -->
            <div class="status-item">
              <div class="status-item-header">
                <span class="status-name">
                  <i
                    class="legend-dot green"
                    aria-hidden="true"
                  ></i>

                  新增用户
                </span>

                <span class="status-value">
                  236
                </span>
              </div>

              <div class="progress">
                <div
                  class="progress-bar green"
                  style="width: 18%"
                ></div>
              </div>
            </div>

            <!-- 已禁用用户 -->
            <div class="status-item">
              <div class="status-item-header">
                <span class="status-name">
                  <i
                    class="legend-dot gray"
                    aria-hidden="true"
                  ></i>

                  已禁用
                </span>

                <span class="status-value">
                  112
                </span>
              </div>

              <div class="progress">
                <div
                  class="progress-bar gray"
                  style="width: 9%"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </article>

      <!-- ==================== 角色分布 ==================== -->
      <article class="panel">
        <header class="panel-header">
          <div class="panel-title">
            <h2>角色分布</h2>
            <p>用户数量最多的角色</p>
          </div>

          <button
            class="panel-action"
            type="button"
          >
            全部角色
          </button>
        </header>

        <div class="role-list">
          <!-- 系统管理员 -->
          <div class="role-item">
            <span class="role-icon">
              管
            </span>

            <div class="role-info">
              <strong>系统管理员</strong>
              <span>拥有全部系统权限</span>
            </div>

            <span class="role-count">
              6 人
            </span>
          </div>

          <!-- 运营人员 -->
          <div class="role-item">
            <span class="role-icon">
              运
            </span>

            <div class="role-info">
              <strong>运营人员</strong>
              <span>日常业务运营角色</span>
            </div>

            <span class="role-count">
              286 人
            </span>
          </div>

          <!-- 审计人员 -->
          <div class="role-item">
            <span class="role-icon">
              审
            </span>

            <div class="role-info">
              <strong>审计人员</strong>
              <span>查看和审计系统数据</span>
            </div>

            <span class="role-count">
              32 人
            </span>
          </div>

          <!-- 普通用户 -->
          <div class="role-item">
            <span class="role-icon">
              普
            </span>

            <div class="role-info">
              <strong>普通用户</strong>
              <span>基础页面访问权限</span>
            </div>

            <span class="role-count">
              962 人
            </span>
          </div>
        </div>
      </article>
    </section>

    <!-- ==================== 底部数据区域 ==================== -->
    <section class="bottom-grid">
      <!-- ==================== 页面数据 ==================== -->
      <article class="panel">
        <header class="panel-header">
          <div class="panel-title">
            <h2>页面数据</h2>
            <p>系统页面配置统计</p>
          </div>

          <button
            class="panel-action"
            type="button"
          >
            页面管理
          </button>
        </header>

        <div class="page-list">
          <!-- 全部页面 -->
          <div class="page-item">
            <div
              class="page-icon"
              aria-hidden="true"
            >
              <i class="bi bi-window"></i>
            </div>

            <div class="page-info">
              <strong>全部页面</strong>
              <span>系统页面总数</span>
            </div>

            <span class="page-number">
              32
            </span>
          </div>

          <!-- 启用页面 -->
          <div class="page-item">
            <div
              class="page-icon"
              aria-hidden="true"
            >
              <i class="bi bi-check-lg"></i>
            </div>

            <div class="page-info">
              <strong>启用页面</strong>
              <span>当前可以正常访问</span>
            </div>

            <span class="page-number">
              30
            </span>
          </div>

          <!-- 一级页面 -->
          <div class="page-item">
            <div
              class="page-icon"
              aria-hidden="true"
            >
              <i class="bi bi-list-ul"></i>
            </div>

            <div class="page-info">
              <strong>一级页面</strong>
              <span>顶级菜单页面</span>
            </div>

            <span class="page-number">
              8
            </span>
          </div>

          <!-- 禁用页面 -->
          <div class="page-item">
            <div
              class="page-icon"
              aria-hidden="true"
            >
              <i class="bi bi-exclamation-circle"></i>
            </div>

            <div class="page-info">
              <strong>禁用页面</strong>
              <span>当前禁止访问</span>
            </div>

            <span class="page-number">
              2
            </span>
          </div>
        </div>
      </article>

      <!-- ==================== 最近新增用户 ==================== -->
      <article class="panel">
        <header class="panel-header">
          <div class="panel-title">
            <h2>最近新增用户</h2>
            <p>最新加入系统的用户</p>
          </div>

          <button
            class="panel-action"
            type="button"
          >
            全部用户
          </button>
        </header>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>用户</th>
                <th>角色</th>
                <th>状态</th>
              </tr>
            </thead>

            <tbody>
              <!-- 用户 1 -->
              <tr>
                <td>
                  <div class="table-user">
                    <span class="table-avatar">
                      陈
                    </span>

                    <strong>陈清远</strong>
                  </div>
                </td>

                <td>系统管理员</td>

                <td>
                  <span class="tag enabled">
                    启用
                  </span>
                </td>
              </tr>

              <!-- 用户 2 -->
              <tr>
                <td>
                  <div class="table-user">
                    <span class="table-avatar">
                      林
                    </span>

                    <strong>林安琪</strong>
                  </div>
                </td>

                <td>运营人员</td>

                <td>
                  <span class="tag enabled">
                    启用
                  </span>
                </td>
              </tr>

              <!-- 用户 3 -->
              <tr>
                <td>
                  <div class="table-user">
                    <span class="table-avatar">
                      周
                    </span>

                    <strong>周子航</strong>
                  </div>
                </td>

                <td>审计人员</td>

                <td>
                  <span class="tag disabled">
                    禁用
                  </span>
                </td>
              </tr>

              <!-- 用户 4 -->
              <tr>
                <td>
                  <div class="table-user">
                    <span class="table-avatar">
                      许
                    </span>

                    <strong>许知夏</strong>
                  </div>
                </td>

                <td>普通用户</td>

                <td>
                  <span class="tag enabled">
                    启用
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </article>
    </section>
  </div>
</template>

<!-- ==================== 系统概览样式 ==================== -->
<style
  scoped
  lang="scss"
  src="./dashboard.scss"
></style>