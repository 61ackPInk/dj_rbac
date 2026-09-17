import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import { loginApi, getCurrentUserApi } from '@/api/auth'
import {
  getAccessToken,
  saveTokens,
  clearTokens,
} from '@/utils/token'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(getAccessToken())
  const user = ref(null)

  // 只表示本地存在登录凭证，不代表后端已确认凭证有效。
  // 真正的身份和权限始终由后端校验。
  const isLoggedIn = computed(() => Boolean(accessToken.value))

  const login = async (formData) => {
    // request 已经取出了响应里的 data，这里不用再写 result.data
    const result = await loginApi(formData)

    saveTokens(result.access_token, result.refresh_token)
    accessToken.value = result.access_token
    user.value = result.user

    return result
  }

  // 刷新页面后，内存里的 user 会丢失。
  // 后续可通过这个方法重新向后端获取用户资料。
  const fetchCurrentUser = async () => {
    user.value = await getCurrentUserApi()
    return user.value
  }

  const clearSession = () => {
    clearTokens()
    accessToken.value = ''
    user.value = null
  }

  // 必须返回，组件才能通过 auth.login() 等方式访问
  return {
    accessToken,
    user,
    isLoggedIn,
    login,
    fetchCurrentUser,
    clearSession,
  }
})