import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

export default defineComponent({
  name: 'HomeView',

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const logoutLoading = ref(false)

    const handleLogout = async () => {
      // 防止连续点击导致重复退出
      if (logoutLoading.value) return

      logoutLoading.value = true

      try {
        await authStore.logout()

        message.success('退出登录成功')

        /*
         * replace 不保留当前后台页面记录，
         * 避免点击浏览器返回按钮又回到退出前页面。
         */
        await router.replace({
          name: 'login',
        })
      } catch (error) {
        message.error(
          error.userMessage ||
            '退出登录失败，请稍后重试',
        )
      } finally {
        logoutLoading.value = false
      }
    }

    return {
      user: authStore.user,
      logoutLoading,
      handleLogout,
    }
  },
})