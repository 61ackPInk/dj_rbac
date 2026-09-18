const THEME_KEY = 'theme'

// 以后新增主题，要把对应名称加入这里
const SUPPORTED_THEMES = ['light', 'dark']

export const setTheme = (theme) => {
  // 防止存储或调用时传入不存在的主题
  const selectedTheme = SUPPORTED_THEMES.includes(theme)
    ? theme
    : 'light'

  // 修改 html 的属性，触发对应主题的 CSS 变量
  document.documentElement.dataset.theme = selectedTheme

  // Element Plus 官方深色样式通过 dark 类启用
  document.documentElement.classList.toggle(
    'dark',
    selectedTheme === 'dark',
  )

  // 主题偏好可以长期保存；不包含登录凭证
  localStorage.setItem(THEME_KEY, selectedTheme)
}

export const initTheme = () => {
  setTheme(localStorage.getItem(THEME_KEY) || 'light')
}