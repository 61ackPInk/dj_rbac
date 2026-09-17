<script setup>
import { ElMessage } from 'element-plus'

// 点击按钮，验证组件库和中文提示是否正常工作
const handleTest = () => {
  ElMessage.success('前端基础配置成功')
}
</script>

<template>
  <main class="home-page">
    <el-card class="welcome-card">
      <template #header>
        <div class="card-title">
          <i class="bi bi-shield-lock"></i>
          <span>RBAC 权限管理系统</span>
        </div>
      </template>

      <p>Vue、Router、Pinia 和 Element Plus 已接入。</p>

      <el-button type="primary" @click="handleTest">
        测试提示消息
      </el-button>
    </el-card>
  </main>
</template>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.welcome-card {
  width: 100%;
  max-width: 480px;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>