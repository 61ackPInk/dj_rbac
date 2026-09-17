import axios from 'axios'

const request = axios.create({
  // 接口文件只写 /auth/login/，最终请求路径为 /api/auth/login/
  baseURL: '/api',

  // 请求超过 15 秒仍未完成，按超时处理
  timeout: 15000,
})

// 统一处理后端返回的数据
request.interceptors.response.use(
  (response) => {
    /*
     * 后端返回：
     * {
     *   code: 200,
     *   message: 'success',
     *   data: { ... }
     * }
     *
     * 这里直接返回里面的 data。
     * 因此页面拿到的结果不需要再写 response.data.data。
     */
    return response.data.data
  },

  (error) => {
    /*
     * 后端错误格式：
     * {
     *   code: 400,
     *   message: 'error',
     *   data: null,
     *   errors: { username: ['用户名已存在'] }
     * }
     *
     * 保留原始错误，同时补充便于页面使用的字段。
     */
    error.status = error.response?.status ?? null
    error.validationErrors = error.response?.data?.errors ?? null

    if (error.response) {
      const detail = error.validationErrors?.detail

      // detail 通常用于认证失败、权限不足等错误
      error.userMessage =
        typeof detail === 'string'
          ? detail
          : `请求失败（HTTP ${error.status}），请检查提交内容`
    } else if (error.code === 'ECONNABORTED') {
      error.userMessage = '请求超时，请稍后重试'
    } else {
      error.userMessage = '无法连接服务，请检查网络和后端运行状态'
    }

    // 继续抛出错误，让页面通过 try/catch 决定如何展示
    return Promise.reject(error)
  },
)

export default request