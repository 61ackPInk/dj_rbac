<script>

</script>

<template>
  <!-- 登陆页面 -->
  <div class="login-warp">
    <!-- 左侧 -->
    <div class="login-left">
        <h1 class="title">>WELCOME BACK</h1>
    </div>
    <!-- 右侧 -->
    <div class="login-right">
      <div class="login-card">
        <h2 class="login-title">Login in</h2>
      </div>
    </div>

  </div>
</template>

<style scoped>
.login-warp {
  min-height: 100vh;
  display: flex;

  /* ========== 左侧 ========== */
  .login-left {
    width: 60%;
    height: 100%;
    background: #d4cfcf;
  }

  /* ========== 右侧 ========== */
  .login-right{
    width: 40%;
    height: 100%;
    background: #868080;
  }
}
</style>