const ACCESS_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

// sessionStorage：刷新页面后仍保留，关闭当前标签页后清除
// 不保存用户名密码。
// Token 可被页面脚本读取，因此不要渲染不可信 HTML。
export const getAccessToken = () => {
  return sessionStorage.getItem(ACCESS_TOKEN_KEY) || ''
}

export const saveTokens = (accessToken, refreshToken) => {
  sessionStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  sessionStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
}

export const clearTokens = () => {
  sessionStorage.removeItem(ACCESS_TOKEN_KEY)
  sessionStorage.removeItem(REFRESH_TOKEN_KEY)
}