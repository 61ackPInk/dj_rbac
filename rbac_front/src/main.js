// 这里是入口文件

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'

// 引入组件库、图标和项目全局样式
import 'element-plus/dist/index.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import './assets/styles/main.scss'

import App from './App.vue'
import router from './router'

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
