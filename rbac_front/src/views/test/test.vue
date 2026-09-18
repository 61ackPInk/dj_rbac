<script src="./test.js"></script>

<template>
  <main class="login-page">
    <!-- 纯装饰区域，不参与辅助设备的内容朗读 -->
    <section class="left-panel" aria-hidden="true">
      <div class="decoration circle shape-1"></div>
      <div class="decoration circle shape-2"></div>
      <div class="decoration square shape-3"></div>
      <div class="decoration square shape-4"></div>
      <div class="decoration square shape-5"></div>
      <div class="decoration line line-1"></div>
      <div class="decoration line line-2"></div>
      <div class="dot"></div>

      <div class="left-text">
        <h1>WELCOME BACK</h1>
        <p>Sign in to continue your journey</p>
      </div>
    </section>

    <section class="right-panel" aria-labelledby="login-title">
      <div class="login-card">
        <h2 id="login-title">账号登录</h2>
        <p class="login-subtitle">请输入您的账号信息</p>

        <!-- 使用自己的校验；按钮点击和回车都会触发提交 -->
        <form novalidate :aria-busy="loading" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="login-username">账号</label>
            <div class="input-line">
              <input
                id="login-username"
                v-model="form.username"
                name="username"
                type="text"
                autocomplete="username"
                placeholder="请输入账号"
                maxlength="20"
                required
                :disabled="loading"
                :aria-invalid="Boolean(errors.username)"
                :aria-describedby="errors.username ? 'username-error' : undefined"
              />
            </div>
            <p v-if="errors.username" id="username-error" class="field-error">
              {{ errors.username }}
            </p>
          </div>

          <div class="form-group">
            <label for="login-password">密码</label>
            <div class="input-line">
              <input
                id="login-password"
                v-model="form.password"
                name="password"
                type="password"
                autocomplete="current-password"
                placeholder="请输入密码"
                required
                :disabled="loading"
                :aria-invalid="Boolean(errors.password)"
                :aria-describedby="errors.password ? 'password-error' : undefined"
              />
            </div>
            <p v-if="errors.password" id="password-error" class="field-error">
              {{ errors.password }}
            </p>
          </div>

          <div class="form-options">
            <label>
              <input v-model="rememberAccount" type="checkbox" :disabled="loading" />
              记住账号
            </label>
            <button type="button" class="text-button" @click="showHelp('password')">
              忘记密码？
            </button>
          </div>

          <p v-if="submitError" class="submit-error" role="alert">
            {{ submitError }}
          </p>

          <button type="submit" class="btn-login" :disabled="loading">
            <span>{{ loading ? '登录中…' : '登 录' }}</span>
          </button>
        </form>

        <p v-if="notice" class="notice" role="status">{{ notice }}</p>

        <div class="divider-line"></div>
        <div class="register-tip">
          还没有账号？
          <button type="button" class="text-button" @click="showHelp('register')">
            立即注册
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped lang="scss" src="./test.scss"></style>