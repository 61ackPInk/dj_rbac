<!-- 外部 JS 使用普通 script，不能添加 setup -->
<script src="./login.js"></script>

<template>
    <main class="login-page">
        <!-- 左侧面板 -->
        <div class="left-panel">
            <i class="bi bi-gift"></i>
            
        </div>
        <!-- 右侧面板 -->
        <div class="right-panel">

        </div>
    </main>
</template>

<!-- scoped 保证样式仅作用于当前页面 -->
<style scoped lang="scss">
    .login-page {
        display: flex;
        height: 100vh;
        width: 100vw;
        background-color: var(--app-success);
    }
</style>