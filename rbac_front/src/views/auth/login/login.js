import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

const REMEMBERED_ACCOUNT_KEY = 'remembered_account'

export default defineComponent({
  name: 'LoginView',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    // 如果之前选择了“记住账号”，进入页面时自动填入账号
    const rememberedAccount =
      localStorage.getItem(REMEMBERED_ACCOUNT_KEY) || ''

    const form = reactive({
      username: rememberedAccount,
      password: '',
    })

    const rememberAccount = ref(Boolean(rememberedAccount))
    const showPassword = ref(false)
    const loading = ref(false)

    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    const validateForm = () => {
      if (!form.username) {
        message.warning('请输入账号')
        return false
      }

      if (form.username.length > 20) {
        message.warning('账号最多为 20 个字符')
        return false
      }

      if (/\s/.test(form.username)) {
        message.warning('账号不能包含空白字符')
        return false
      }

      if (!form.password) {
        message.warning('请输入密码')
        return false
      }

      if (/\s/.test(form.password)) {
        message.warning('密码不能包含空白字符')
        return false
      }

      return true
    }

    /*
     * 后端错误可能是：
     * "用户名或密码错误"
     * ["用户名或密码错误"]
     * { non_field_errors: ["用户名或密码错误"] }
     *
     * 递归查找第一条可展示的错误文字。
     */
    const findFirstError = (errors) => {
      if (typeof errors === 'string') {
        return errors
      }

      if (Array.isArray(errors)) {
        for (const item of errors) {
          const result = findFirstError(item)
          if (result) return result
        }

        return ''
      }

      if (errors && typeof errors === 'object') {
        for (const value of Object.values(errors)) {
          const result = findFirstError(value)
          if (result) return result
        }
      }

      return ''
    }

    const saveRememberedAccount = () => {
      if (rememberAccount.value) {
        // 只保存账号，绝不保存用户密码
        localStorage.setItem(
          REMEMBERED_ACCOUNT_KEY,
          form.username,
        )
      } else {
        localStorage.removeItem(REMEMBERED_ACCOUNT_KEY)
      }
    }

    const handleLogin = async () => {
      // 防止用户连续点击按钮，重复提交登录请求
      if (loading.value) return

      if (!validateForm()) return

      loading.value = true

      try {
        /*
         * Store 内部会：
         * 1. 调用 POST /api/auth/login/
         * 2. 保存 access_token 和 refresh_token
         * 3. 保存当前用户信息
         */
        await authStore.login({
          username: form.username,
          password: form.password,
        })

        saveRememberedAccount()

        // 登录完成后立即清空页面内存中的明文密码
        form.password = ''

        message.success('登录成功')

        // replace 防止浏览器返回按钮重新返回登录页
        await router.replace({
          name: 'home',
        })
      } catch (error) {
        const backendMessage = findFirstError(
          error.validationErrors,
        )

        message.error(
          backendMessage ||
            error.userMessage ||
            '登录失败，请稍后重试',
        )
      } finally {
        // 无论登录成功还是失败，都恢复按钮状态
        loading.value = false
      }
    }

    const showUnavailable = (featureName) => {
      message.info(`${featureName}功能暂未开放`)
    }

    /*
     * 普通 setup() 必须返回模板需要使用的内容。
     * 以后模板新增变量或方法，也要在这里返回。
     */
    return {
      form,
      rememberAccount,
      showPassword,
      loading,
      togglePassword,
      handleLogin,
      showUnavailable,
    }
  },
})