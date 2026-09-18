// 这里是入口文件

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 先加载组件库样式
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'

// 加载图标
import 'bootstrap-icons/font/bootstrap-icons.css'

// 最后加载项目样式，覆盖默认主题变量
import './assets/styles/main.scss'


import { initTheme } from '@/utils/theme'
import App from './App.vue'
import router from './router'


// 应用挂载前恢复用户选择的主题
initTheme()

const app = createApp(App)

// Pinia：后续保存登录用户和权限信息
app.use(createPinia())

// Router：管理登录页、后台页面之间的跳转
app.use(router)

// 注册 Element Plus，并使用中文语言包
app.use(ElementPlus, {
  locale: zhCn,
})

app.mount('#app')
