<!-- 外部 JS 使用普通 script，不能添加 setup -->
<script src="./index.js"></script>

<template>
    <main class="login-page">
        <el-card class="login-card">
            <template #header>
                <div class="login-title">
                    <i class="bi bi-shield-lock"></i>
                    <span>RBAC 登录</span>
                </div>
            </template>

            <!-- 使用表单提交事件，按钮点击和输入框回车共用同一方法 -->
            <el-form ref="formRef" :model="form" :rules="rules" label-position="top" @submit.prevent="handleLogin">
                <el-form-item label="用户名" prop="username">
                    <!-- 不使用 .trim，输入空格时直接提示，而不是偷偷删除 -->
                    <el-input v-model="form.username" autocomplete="username" placeholder="请输入用户名" maxlength="20" />
                </el-form-item>

                <el-form-item label="密码" prop="password">
                    <el-input v-model="form.password" type="password" autocomplete="current-password"
                        placeholder="请输入密码" show-password />
                </el-form-item>

                <el-button class="login-button" type="primary" native-type="submit" :loading="loading">
                    登录
                </el-button>
            </el-form>
        </el-card>
    </main>
</template>

<!-- scoped 保证样式仅作用于当前页面 -->
<style scoped lang="scss" src="./index.scss"></style>