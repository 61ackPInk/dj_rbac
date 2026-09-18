import { defineComponent, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const REMEMBERED_ACCOUNT_KEY = 'remembered_account'

export default defineComponent({
  name: 'LoginView',

  setup() {
    const router = useRouter()
    const auth = useAuthStore()

    const savedAccount = localStorage.getItem(REMEMBERED_ACCOUNT_KEY) || ''

    const form = reactive({
      username: savedAccount,
      password: '',
    })

    const errors = reactive({
      username: '',
      password: '',
    })

    const rememberAccount = ref(Boolean(savedAccount))
    const loading = ref(false)
    const submitError = ref('')
    const notice = ref('')

    // 不自动 trim：空白字符应提示错误，而不是悄悄修改用户输入
    const validateForm = () => {
      errors.username = ''
      errors.password = ''

      if (!form.username) {
        errors.username = '请输入账号'
      } else if (form.username.length > 20) {
        errors.username = '账号最多 20 个字符'
      } else if (/\s/.test(form.username)) {
        errors.username = '账号不能包含空白字符'
      }

      if (!form.password) {
        errors.password = '请输入密码'
      } else if (/\s/.test(form.password)) {
        errors.password = '密码不能包含空白字符'
      }

      return !errors.username && !errors.password
    }

    const handleLogin = async () => {
      if (loading.value) return

      submitError.value = ''
      notice.value = ''

      if (!validateForm()) return

      loading.value = true

      try {
        // 沿用公共 Store，不在页面里重复保存 Token
        await auth.login({
          username: form.username,
          password: form.password,
        })
      } catch (error) {
        const backendErrors = error.validationErrors || {}

        /*
         * 逐个检查账号和密码字段。
         * 后端字段错误显示在对应输入框下面，
         * 而不是把所有错误混成一条提示。
         */
        for (const field of ['username', 'password']) {
          const value = backendErrors[field]
          const message = Array.isArray(value) ? value[0] : value

          if (typeof message === 'string') {
            errors[field] = message
          }
        }

        // 用户名或密码错误通常位于 non_field_errors
        const generalErrors = backendErrors.non_field_errors
        const generalMessage = Array.isArray(generalErrors)
          ? generalErrors[0]
          : generalErrors

        if (typeof generalMessage === 'string') {
          submitError.value = generalMessage
        } else if (!errors.username && !errors.password) {
          submitError.value = error.userMessage || '登录失败，请稍后重试'
        }

        return
      } finally {
        loading.value = false
      }

      // 只保存账号；密码始终不写入浏览器存储
      if (rememberAccount.value) {
        localStorage.setItem(REMEMBERED_ACCOUNT_KEY, form.username)
      } else {
        localStorage.removeItem(REMEMBERED_ACCOUNT_KEY)
      }

      form.password = ''
      await router.replace({ name: 'home' })
    }

    const showHelp = (type) => {
      notice.value =
        type === 'password'
          ? '找回密码功能暂未开放，请联系管理员。'
          : '注册页面暂未接入，请联系管理员创建账号。'
    }

    // 外部普通 script 的 setup 必须返回模板使用的变量和方法
    return {
      form,
      errors,
      rememberAccount,
      loading,
      submitError,
      notice,
      handleLogin,
      showHelp,
    }
  },
})