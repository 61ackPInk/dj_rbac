import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [vue(), vueDevTools()],

  resolve: {
    alias: {
      // 后续可以使用 @/api/auth，代替 ../../api/auth
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },

  server: {
    proxy: {
      // 浏览器请求 /api/... 时，由 Vite 转发给 Django
      // 保留 /api 前缀，因为后端路由本身就包含 /api/
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})