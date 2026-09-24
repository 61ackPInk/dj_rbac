<!-- ==================== 登录页业务逻辑 ==================== -->
<script src="./login.js"></script>

<template>
  <main class="login-page">
    <!-- ==================== 背景装饰 ==================== -->
    <span
      class="background-shape background-shape--top"
      aria-hidden="true"
    ></span>

    <span
      class="background-shape background-shape--bottom"
      aria-hidden="true"
    ></span>

    <!-- ==================== 页面品牌 ==================== -->
    <header class="page-brand">
      <div
        class="brand-logo"
        aria-hidden="true"
      >
        <i class="bi bi-grid"></i>
      </div>

      <span class="brand-name">
        BP Workbench
      </span>
    </header>

    <!-- ==================== 登录卡片 ==================== -->
    <section
      class="login-card"
      aria-labelledby="login-title"
    >
      <!-- 登录卡片头部 -->
      <header class="card-header">
        <div
          class="welcome-icon"
          aria-hidden="true"
        >
          <i class="bi bi-shield-lock"></i>
        </div>

        <h1 id="login-title">
          欢迎登录
        </h1>

        <p>
          登录 BP Workbench，开始管理你的工作空间
        </p>
      </header>

      <!-- ==================== 登录表单 ==================== -->
      <form
        novalidate
        @submit.prevent="handleLogin"
      >
        <!-- 用户名 -->
        <label class="form-field">
          <span class="field-label">
            用户名
          </span>

          <span class="input-wrapper">
            <i
              class="bi bi-person input-icon"
              aria-hidden="true"
            ></i>

            <input
              v-model.trim="form.username"
              name="username"
              type="text"
              maxlength="20"
              autocomplete="username"
              placeholder="请输入用户名"
            />
          </span>
        </label>

        <!-- 密码 -->
        <label class="form-field">
          <span class="field-label">
            密码
          </span>

          <span class="input-wrapper">
            <i
              class="bi bi-lock input-icon"
              aria-hidden="true"
            ></i>

            <input
              v-model="form.password"
              name="password"
              :type="showPassword ? 'text' : 'password'"
              autocomplete="current-password"
              placeholder="请输入密码"
            />

            <!-- 显示或隐藏密码 -->
            <button
              class="password-toggle"
              type="button"
              :aria-label="showPassword ? '隐藏密码' : '显示密码'"
              :title="showPassword ? '隐藏密码' : '显示密码'"
              @click="togglePassword"
            >
              <i
                class="bi"
                :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"
                aria-hidden="true"
              ></i>
            </button>
          </span>
        </label>

        <!-- ==================== 表单辅助操作 ==================== -->
        <div class="form-options">
          <!-- 只保存用户名，不保存用户密码 -->
          <label class="remember-option">
            <input
              v-model="rememberAccount"
              type="checkbox"
              name="remember"
            />

            <span>记住账号</span>
          </label>

          <button
            class="text-button"
            type="button"
            @click="showUnavailable('找回密码')"
          >
            忘记密码？
          </button>
        </div>

        <!--
          预留表单提示区域。
          当前登录错误继续使用项目已有的消息提示。
        -->
        <p
          class="form-message"
          aria-live="polite"
        ></p>

        <!-- ==================== 登录按钮 ==================== -->
        <button
          class="login-button"
          type="submit"
          :disabled="loading"
        >
          <span>
            {{ loading ? '登录中...' : '登录' }}
          </span>

          <i
            class="bi bi-arrow-right"
            aria-hidden="true"
          ></i>
        </button>
      </form>

      <!-- ==================== 登录帮助 ==================== -->
      <footer class="card-footer">
        登录遇到问题？

        <button
          type="button"
          @click="showUnavailable('联系管理员')"
        >
          联系管理员
        </button>
      </footer>
    </section>

    <!-- ==================== 页面底部 ==================== -->
    <footer class="page-footer">
      © 2026 BP Workbench
    </footer>
  </main>
</template>

<!-- ==================== 登录页样式 ==================== -->
<style
  scoped
  lang="scss"
  src="./login.scss"
></style>