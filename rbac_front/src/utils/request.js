import axios from 'axios'

import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveAccessToken,
} from '@/utils/token'

const request = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

/*
 * 刷新 Token 使用独立的 Axios 实例。
 *
 * 不能使用 request 调用刷新接口，
 * 否则刷新接口自己返回 401 时，
 * 会再次进入当前响应拦截器，造成循环刷新。
 */
const refreshRequest = axios.create({
  baseURL: '/api',
  timeout: 15000,
})

// 不需要携带 access_token 的公开接口
const PUBLIC_URLS = [
  '/auth/login/',
  '/auth/register/',
  '/auth/refresh/',
]

// 保存正在进行的刷新请求
// 多个接口同时返回 401 时，只刷新一次 Token
let refreshPromise = null

const isPublicRequest = (url = '') => {
  return PUBLIC_URLS.includes(url)
}

const refreshAccessToken = async () => {
  const refreshToken = getRefreshToken()

  if (!refreshToken) {
    throw new Error('缺少 refresh_token')
  }

  /*
   * 如果已经有刷新请求正在进行，
   * 后续接口直接等待同一个请求结果。
   */
  if (refreshPromise) {
    return refreshPromise
  }

  refreshPromise = refreshRequest
    .post('/auth/refresh/', {
      refresh_token: refreshToken,
    })
    .then((response) => {
      /*
       * 自定义 Renderer 返回：
       * {
       *   code: 200,
       *   message: 'success',
       *   data: {
       *     access_token: '...'
       *   }
       * }
       */
      const newAccessToken =
        response.data?.data?.access_token

      if (!newAccessToken) {
        throw new Error('刷新接口没有返回 access_token')
      }

      saveAccessToken(newAccessToken)

      return newAccessToken
    })
    .finally(() => {
      /*
       * 成功或失败后都清空，
       * 允许以后再次发起刷新请求。
       */
      refreshPromise = null
    })

  return refreshPromise
}

const redirectToLogin = () => {
  // 已经在登录页时不重复跳转
  if (window.location.pathname === '/login') {
    return
  }

  /*
   * 保存用户原本所在的网址。
   * 重新登录后可以通过 redirect 返回原页面。
   */
  const currentPath =
    window.location.pathname +
    window.location.search +
    window.location.hash

  const loginUrl =
    `/login?redirect=${encodeURIComponent(currentPath)}`

  /*
   * Token 刷新失败属于登录状态完全失效。
   * 这里刷新一次页面，同时清空 Pinia 内存状态。
   */
  window.location.replace(loginUrl)
}

// 请求拦截器：自动添加 access_token
request.interceptors.request.use((config) => {
  const accessToken = getAccessToken()

  if (
    accessToken &&
    !isPublicRequest(config.url)
  ) {
    config.headers.Authorization =
      `Bearer ${accessToken}`
  }

  return config
})

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    // 页面直接获得 Renderer 中的 data
    return response.data.data
  },

  async (error) => {
    const originalRequest = error.config
    const status = error.response?.status ?? null

    /*
     * 以下条件同时满足时尝试刷新：
     *
     * 1. 后端返回 401；
     * 2. 存在原请求配置；
     * 3. 不是登录、注册、刷新等公开接口；
     * 4. 当前请求还没有重试过。
     */
    const shouldRefresh =
      status === 401 &&
      originalRequest &&
      !isPublicRequest(originalRequest.url) &&
      !originalRequest._retry

    if (shouldRefresh) {
      // 标记已经重试过，防止无限循环
      originalRequest._retry = true

      try {
        const newAccessToken =
          await refreshAccessToken()

        /*
         * 给原请求换上新的 Token，
         * 然后自动重新发送刚才失败的请求。
         */
        originalRequest.headers.Authorization =
          `Bearer ${newAccessToken}`

        return request(originalRequest)
      } catch (refreshError) {
        /*
         * refresh_token 过期、被撤销或用户已禁用时，
         * 清除本地凭证并重新登录。
         */
        clearTokens()
        redirectToLogin()

        return Promise.reject(refreshError)
      }
    }

    /*
     * 不需要刷新 Token 的普通错误，
     * 继续整理成页面容易使用的格式。
     */
    error.status = status
    error.validationErrors =
      error.response?.data?.errors ?? null

    if (error.response) {
      const detail =
        error.validationErrors?.detail

      error.userMessage =
        typeof detail === 'string'
          ? detail
          : `请求失败（HTTP ${status}），请检查提交内容`
    } else if (error.code === 'ECONNABORTED') {
      error.userMessage = '请求超时，请稍后重试'
    } else {
      error.userMessage =
        '无法连接服务，请检查网络和后端运行状态'
    }

    return Promise.reject(error)
  },
)

export default request