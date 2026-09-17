<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
})

// 用户名和密码都禁止空白字符，包括空格、换行和制表符
const validateNoWhitespace = (rule, value, callback) => {
  if (/\s/.test(value)) {
    callback(new Error(`${rule.label}不能包含空白字符`))
    return
  }

  callback()
}

// prop 必须与 form 字段名称一致，才能触发对应字段的校验
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { max: 20, message: '用户名最多 20 个字符', trigger: 'blur' },
    {
      validator: validateNoWhitespace,
      label: '用户名',
      trigger: 'blur',
    },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    {
      validator: validateNoWhitespace,
      label: '密码',
      trigger: 'blur',
    },
  ],
}

const handleLogin = async () => {
  // 按钮和回车都可以提交，需要避免重复发送请求
  if (loading.value || !formRef.value) return

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true

  try {
    await auth.login({
      username: form.username,
      password: form.password,
    })
  } catch (error) {
    /*
     * 后端可能返回：
     * { username: ['...'] }
     * 或 { non_field_errors: ['用户名或密码错误'] }
     *
     * 收集第一条错误用于展示。
     * Object.values 是遍历错误对象的各字段值。
     * flat 将各字段的错误数组合并成一层数组。
     */
    const messages = Object.values(error.validationErrors || {}).flat()
    const message = messages.find((item) => typeof item === 'string')

    ElMessage.error(message || error.userMessage || '登录失败')
    return
  } finally {
    // 成功或失败都会执行，恢复按钮状态
    loading.value = false
  }

  ElMessage.success('登录成功')

  // replace 替换登录页记录，避免返回按钮再次回到登录表单
  await router.replace({ name: 'home' })
}
</script>

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
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <!-- 不使用 .trim，输入空格时直接提示，而不是偷偷删除 -->
          <el-input
            v-model="form.username"
            autocomplete="username"
            placeholder="请输入用户名"
            maxlength="20"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            type="password"
            autocomplete="current-password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-button
          class="login-button"
          type="primary"
          native-type="submit"
          :loading="loading"
        >
          登录
        </el-button>
      </el-form>
    </el-card>
  </main>
</template>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.login-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 20px;
}

.login-button {
  width: 100%;
}
</style>