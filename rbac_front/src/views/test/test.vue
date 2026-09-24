<script>

</script>

<template>
  <!-- 登陆页面 -->
  <div class="login-warp">
    <!-- 左侧 -->
    <!-- <div class="login-left">
        <h1 class="title">WELCOME BACK</h1>
    </div> -->
    <!-- 右侧 -->
    <!-- <div class="login-right">
      <div class="login-card">
        <h2 class="login-title">Login in</h2>
      </div>
    </div> -->
    <div class="brand">
      <div class="brand-logo">
        <i class="bi bi-slack"></i>
      </div>
      <div class="brand-name">
        BP Workbench
      </div>
    </div>
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">
          <i class="bi bi-shield-lock"></i>
        </div>
        <div class="login-title">
          <h2>欢迎登录</h2>
        </div>
        <div class="login-description">
          <p>登录 BP Workbench，开始管理你的工作空间</p>
        </div>
      </div>
      <div class="login-form">

      </div>
    </div>
  </div>
</template>

<style scoped>
.login-warp {
  min-height: 100vh;
  background: var(--bg-page);
  display: flex;
  align-items: center;
  justify-content: center;

  /* ==================== 网站Brand ==================== */
  .brand {
    position: absolute;
    top: 25px;
    left: 30px;
    display: flex;
    align-items: center;
    gap: 10px;

    .brand-logo {
      display: grid;
      place-items: center;
      width: 34px;
      height: 34px;
      color: #fff;
      background: var(--primary);
      border-radius: 10px;
      box-shadow: 0 8px 18px rgba(82, 103, 232, 0.22);
    }

    .brand-name {
      font-size: 17px;
      font-weight: 650;
      letter-spacing: -0.2px;
    }
  }

  /* ==================== 登录卡片 ==================== */
  .login-card {
    width: min(380px, 100%);
    padding: 42px 40px 34px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    box-shadow:
      0 2px 5px rgba(32, 36, 44, 0.02),
      0 18px 50px rgba(32, 36, 44, 0.07);


    /* 头部 */
    .login-header {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 10px;

      .login-icon {
        display: grid;
        place-items: center;
        width: 45px;
        height: 45px;
        color: var(--primary);
        background: var(--primary-light);
        border-radius: 10px;
        /* box-shadow: 0 8px 18px rgba(82, 103, 232, 0.22); */
      }

      .login-title {
        h2 {
          font-size: 26px;
          font-weight: 650;
          line-height: 1.3;
          letter-spacing: -0.6px;
        }
      }

      .login-description {
        color: var(--text-sub);
        font-size: 13px;
        line-height: 1.7;
      }
    }
  }
}
</style>