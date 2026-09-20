const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

// 获取短期访问凭证
export const getAccessToken = () => {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY) || ''
}

// 获取长期刷新凭证
export const getRefreshToken = () => {
  return sessionStorage.getItem(REFRESH_TOKEN_KEY) || ''
}

// 登录成功时，同时保存两个 Token
export const saveTokens = (
  accessToken,
  refreshToken,
) => {
  sessionStorage.setItem(
    ACCESS_TOKEN_KEY,
    accessToken,
  )

  sessionStorage.setItem(
    REFRESH_TOKEN_KEY,
    refreshToken,
  )
}

// 自动刷新时，后端只返回新的 access_token
// refresh_token 保持原值，所以单独提供这个方法
export const saveAccessToken = (accessToken) => {
  sessionStorage.setItem(
    ACCESS_TOKEN_KEY,
    accessToken,
  )
}

// 退出登录或刷新失败时清除所有凭证
export const clearTokens = () => {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY)
  sessionStorage.removeItem(REFRESH_TOKEN_KEY)
}