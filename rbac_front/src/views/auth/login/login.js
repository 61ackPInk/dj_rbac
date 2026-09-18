import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { useAuthStore } from '@/stores/auth'

export default defineComponent({
  name: 'LoginView',

  setup() {
    // 原来 <script setup> 中的变量、校验规则、方法，
    // 全部放到这里。
    const router = useRouter()
    const auth = useAuthStore()

    const formRef = ref(null)
    const loading = ref(false)

    const form = reactive({
      username: '',
      password: '',
    })

    const validateNoWhitespace = (rule, value, callback) => {
      if (/\s/.test(value)) {
        callback(new Error(`${rule.label}不能包含空白字符`))
        return
      }

      callback()
    }

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
        const messages = Object.values(error.validationErrors || {}).flat()
        const message = messages.find((item) => typeof item === 'string')

        ElMessage.error(message || error.userMessage || '登录失败')
        return
      } finally {
        loading.value = false
      }

      ElMessage.success('登录成功')
      await router.replace({ name: 'home' })
    }

    // 普通 setup() 必须返回模板使用的变量和方法。
    // 以后新增供模板使用的内容，也要添加到这里。
    return {
      formRef,
      loading,
      form,
      rules,
      handleLogin,
    }
  },
})