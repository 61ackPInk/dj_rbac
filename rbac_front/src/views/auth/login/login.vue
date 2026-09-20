<script src="./login.js"></script>

<template>
  <div class="login-warp">
    <!-- 左侧内容，移动端隐藏 -->
    <div class="login-left">
      <div class="left-content">
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
      </div>
    </div>

    <!-- 右侧登录区域 -->
    <div class="login-right">
      <div class="login-card">
        <h2 class="title">账户登录</h2>
        <div class="sub-desc">请输入你的账号信息登录系统</div>

        <!--
          使用 form 的 submit 事件：
          点击登录按钮或者在输入框中按 Enter，都会执行 handleLogin。
        -->
        <form novalidate @submit.prevent="handleLogin">
          <!-- 账号 -->
          <div class="form-item">
            <div class="input-wrap">
              <i class="bi bi-person" aria-hidden="true"></i>

              <input
                v-model="form.username"
                class="username-input"
                type="text"
                name="username"
                maxlength="20"
                autocomplete="username"
                placeholder="请输入账号"
              />
            </div>
          </div>

          <!-- 密码 -->
          <div class="form-item">
            <div class="input-wrap">
              <i class="bi bi-lock" aria-hidden="true"></i>

              <input
                v-model="form.password"
                class="password-input"
                :type="showPassword ? 'text' : 'password'"
                name="password"
                autocomplete="current-password"
                placeholder="请输入密码"
                
              />

              <!-- type="button" 防止点击眼睛图标时提交表单 -->
              <button
                type="button"
                class="password-toggle"
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
            </div>
          </div>

          <!-- 只记住账号，不在浏览器中保存密码 -->
          <div class="form-row-between">
            <label>
              <input
                v-model="rememberAccount"
                type="checkbox"
                
              />
              记住账号
            </label>

            <button
              type="button"
              class="text-link"
              @click="showUnavailable('找回密码')"
            >
              忘记密码？
            </button>
          </div>

          <!-- 登录主按钮 -->
          <div class="form-item">
            <button
              type="submit"
              class="btn-login"
              :disabled="loading"
            >
              <span>登录</span>
            </button>
          </div>
        </form>

        <!-- 分隔线 -->
        <div class="divider">
          <span>或使用以下方式登录</span>
        </div>

        <!-- 第三方登录按钮组 -->
        <div class="form-item social-login">
          <button
            type="button"
            class="social-btn"
            @click="showUnavailable('GitHub 登录')"
          >
            <i class="bi bi-github" aria-hidden="true"></i>
            GitHub
          </button>

          <button
            type="button"
            class="social-btn"
            @click="showUnavailable('微信登录')"
          >
            <i class="bi bi-wechat" aria-hidden="true"></i>
            微信
          </button>
        </div>

        <!-- 注册跳转提示 -->
        <div class="tip-text">
          还没有账号？
          <button
            type="button"
            class="text-link link-text"
            @click="showUnavailable('用户注册')"
          >
            立即注册
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss" src="./login.scss"></style>