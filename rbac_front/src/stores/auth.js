import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import {
  loginApi,
  getCurrentUserApi,
} from '@/api/auth'

import {
  getAccessToken,
  saveTokens,
  clearTokens,
} from '@/utils/token'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(getAccessToken())
  const user = ref(null)

  // 是否已经检查过当前登录状态
  const initialized = ref(false)

  /*
   * 防止多个路由同时执行初始化时，
   * 重复请求 /api/auth/me/。
   */
  let initializePromise = null

  // 本地是否存在 access_token
  const hasAccessToken = computed(() => {
    return Boolean(accessToken.value)
  })

  /*
   * 当前是否处于登录状态。
   *
   * 登录成功后有 Token 和用户信息；
   * 页面刷新时先通过 initializeAuth() 恢复用户信息。
   */
  const isLoggedIn = computed(() => {
    return Boolean(accessToken.value && user.value)
  })

  const login = async (formData) => {
    /*
     * request.js 已经取出了后端响应中的 data，
     * 因此这里直接读取 result.access_token。
     */
    const result = await loginApi(formData)

    saveTokens(
      result.access_token,
      result.refresh_token,
    )

    accessToken.value = result.access_token
    user.value = result.user
    initialized.value = true

    return result
  }

  const fetchCurrentUser = async () => {
    const result = await getCurrentUserApi()

    user.value = result

    return result
  }

  const clearSession = () => {
    clearTokens()

    accessToken.value = ''
    user.value = null
  }

  const initializeAuth = async () => {
    // 已经初始化过，不再重复请求
    if (initialized.value) {
      return
    }

    /*
     * 如果初始化请求正在进行，
     * 后续调用复用同一个 Promise。
     */
    if (initializePromise) {
      return initializePromise
    }

    initializePromise = (async () => {
      try {
        if (!hasAccessToken.value) {
          // 本地没有 Token，不需要请求当前用户接口
          user.value = null
          return
        }

        /*
         * 页面刷新后 Pinia 内存中的 user 会丢失，
         * 使用本地 Token 请求后端恢复用户资料。
         */
        await fetchCurrentUser()
      } catch (error) {
        /*
         * 401 表示 Token 不存在、过期、伪造或已经失效。
         * 此时清除本地登录信息。
         *
         * 网络故障等其他错误暂时不清除 Token，
         * 避免因为临时断网强制用户退出。
         */
        if (error.status === 401) {
          clearSession()
        }

        throw error
      } finally {
        initialized.value = true
        initializePromise = null
      }
    })()

    return initializePromise
  }

  return {
    accessToken,
    user,
    initialized,
    hasAccessToken,
    isLoggedIn,

    login,
    fetchCurrentUser,
    initializeAuth,
    clearSession,
  }
})