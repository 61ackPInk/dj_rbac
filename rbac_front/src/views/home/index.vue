<script src="./index.js"></script>

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

<style scoped lang="scss" src="./index.scss"></style>