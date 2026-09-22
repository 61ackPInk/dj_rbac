import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getUsersApi } from '@/api/users'
import { getRolesApi } from '@/api/roles'
import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { message } from '@/utils/message'

export default defineComponent({
  name: 'SystemDashboard',

  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    const navigationStore = useNavigationStore()

    /* ==================== 后端页面信息 ==================== */
    const currentPage = computed(() =>
      navigationStore.pages.find(
        (page) => page.path === route.path,
      ),
    )

    const parentPage = computed(() =>
      navigationStore.pages.find(
        (page) => page.id === currentPage.value?.parent_id,
      ),
    )

    /* ==================== 真实统计数据 ==================== */
    const isRoot = computed(
      () => Boolean(authStore.user?.is_root),
    )

    // null 表示尚未获取成功，区别于真实的 0
    const userCount = ref(null)
    const roleCount = ref(null)
    const loading = ref(false)

    const visiblePageCount = computed(() =>
      navigationStore.loaded
        ? navigationStore.pages.length
        : null,
    )

    onMounted(async () => {
      loading.value = true

      const requests = [
        getRolesApi().then((roles) => {
          roleCount.value = roles.length
        }),
      ]

      // 用户列表接口只有根管理员有权限调用
      if (isRoot.value) {
        requests.push(
          getUsersApi().then((users) => {
            userCount.value = users.length
          }),
        )
      }

      const results = await Promise.allSettled(requests)

      if (results.some((result) => result.status === 'rejected')) {
        message.error('部分统计数据加载失败')
      }

      loading.value = false
    })

    return {
      currentPage,
      parentPage,
      isRoot,
      userCount,
      roleCount,
      visiblePageCount,
      loading,
    }
  },
})