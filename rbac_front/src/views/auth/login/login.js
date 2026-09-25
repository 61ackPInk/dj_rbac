/* ==================== Vue 相关依赖 ==================== */
import {
  defineComponent,
  reactive,
  ref,
} from 'vue'

import {
  useRoute,
  useRouter,
} from 'vue-router'

/* ==================== 项目内部依赖 ==================== */
import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

/* ==================== 本地存储配置 ==================== */

/*
 * 记住账号时使用的 localStorage 键名。
 *
 * 注意：
 * 这里只保存用户名，不保存用户密码。
 */
const REMEMBERED_ACCOUNT_KEY = 'remembered_account'

export default defineComponent({
  name: 'LoginView',

  setup() {
    /* ==================== 路由与状态仓库 ==================== */
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()

    /* ==================== 初始化记住的账号 ==================== */

    /*
     * 如果用户之前选择了“记住账号”，
     * 再次进入登录页时自动填入用户名。
     */
    const rememberedAccount =
      localStorage.getItem(REMEMBERED_ACCOUNT_KEY) || ''

    /* ==================== 登录表单状态 ==================== */
    const form = reactive({
      username: rememberedAccount,
      password: '',
    })

    // 是否记住当前用户名
    const rememberAccount = ref(Boolean(rememberedAccount))

    // 是否显示明文密码
    const showPassword = ref(false)

    // 是否正在提交登录请求
    const loading = ref(false)

    /* ==================== 密码显示控制 ==================== */

    /*
     * 切换密码输入框的显示状态。
     */
    const togglePassword = () => {
      showPassword.value = !showPassword.value
    }

    /* ==================== 登录表单验证 ==================== */

    /*
     * 提交登录请求前进行基础验证。
     *
     * 返回 true 表示允许提交；
     * 返回 false 表示表单存在错误。
     */
    const validateForm = () => {
      if (!form.username) {
        message.warning('请输入用户名')
        return false
      }

      if (form.username.length > 20) {
        message.warning('用户名最多为 20 个字符')
        return false
      }

      if (/\s/.test(form.username)) {
        message.warning('用户名不能包含空白字符')
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

    /* ==================== 后端错误解析 ==================== */

    /*
     * 后端返回的错误可能存在多种格式：
     *
     * "用户名或密码错误"
     *
     * ["用户名或密码错误"]
     *
     * {
     *   non_field_errors: ["用户名或密码错误"],
     * }
     *
     * 递归查找其中第一条可以显示的错误文字。
     */
    const findFirstError = (errors) => {
      if (typeof errors === 'string') {
        return errors
      }

      if (Array.isArray(errors)) {
        for (const item of errors) {
          const result = findFirstError(item)

          if (result) {
            return result
          }
        }

        return ''
      }

      if (errors && typeof errors === 'object') {
        for (const value of Object.values(errors)) {
          const result = findFirstError(value)

          if (result) {
            return result
          }
        }
      }

      return ''
    }

    /* ==================== 记住账号 ==================== */

    /*
     * 根据用户的选择保存或删除用户名。
     *
     * 为了安全，不允许在 localStorage 中保存密码。
     */
    const saveRememberedAccount = () => {
      if (rememberAccount.value) {
        localStorage.setItem(
          REMEMBERED_ACCOUNT_KEY,
          form.username,
        )

        return
      }

      localStorage.removeItem(REMEMBERED_ACCOUNT_KEY)
    }

    /* ==================== 登录提交 ==================== */

    /*
     * 登录流程：
     *
     * 1. 防止重复提交。
     * 2. 验证用户名和密码。
     * 3. 调用 Pinia 中的登录方法。
     * 4. 保存用户选择的账号。
     * 5. 清除页面内存中的明文密码。
     * 6. 跳转到登录前页面或系统首页。
     */
    const handleLogin = async () => {
      // 登录请求未完成时，不允许重复提交
      if (loading.value) {
        return
      }

      if (!validateForm()) {
        return
      }

      loading.value = true

      try {
        /*
         * authStore.login() 内部会：
         *
         * 1. 调用 POST /api/auth/login/。
         * 2. 保存 access_token 和 refresh_token。
         * 3. 保存当前登录用户的信息。
         */
        await authStore.login({
          username: form.username,
          password: form.password,
        })

        saveRememberedAccount()

        /*
         * 登录完成后立即清除页面内存中的明文密码，
         * 减少密码在前端内存中的保留时间。
         */
        form.password = ''

        message.success('登录成功')

        const redirect = route.query.redirect

        /*
         * redirect 必须是站内绝对路径。
         *
         * 这样可以防止攻击者构造外部网址，
         * 将登录成功的用户跳转到恶意网站。
         */
        const isSafeRedirect =
          typeof redirect === 'string' &&
          redirect.startsWith('/') &&
          !redirect.startsWith('//')

        if (isSafeRedirect) {
          await router.replace(redirect)
          return
        }

        // 没有原访问页面时，进入系统首页
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
        /*
         * 无论登录成功还是失败，
         * 都必须恢复按钮的可用状态。
         */
        loading.value = false
      }
    }

    /* ==================== 暂未开放功能提示 ==================== */

    /*
     * 忘记密码和联系管理员暂未接入真实功能，
     * 点击时显示统一提示。
     */
    const showUnavailable = (featureName) => {
      message.info(`${featureName}功能暂未开放`)
    }

    /* ==================== 向模板暴露数据和方法 ==================== */

    /*
     * 当前使用普通 setup()。
     *
     * 模板需要使用的数据和方法，
     * 都必须在这里显式返回。
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