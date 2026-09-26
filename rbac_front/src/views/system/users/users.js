import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getUsersApi } from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import AppModal from '@/components/feedback/modal/app-modal.vue'

export default defineComponent({
  name: 'SystemUsers',

  /* ==================== 页面使用的公共组件 ==================== */
  components: {
    AppModal,
  },

  setup() {
    const route = useRoute()
    const authStore = useAuthStore()
    const navigationStore = useNavigationStore()

    /* ==================== 后端页面名称 ==================== */
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

    /* ==================== 用户列表状态 ==================== */
    const users = ref([])
    const loading = ref(false)
    const errorMessage = ref('')

    const loadUsers = async () => {
      errorMessage.value = ''

      // 当前用户列表接口只允许根管理员调用
      if (!authStore.user?.is_root) {
        errorMessage.value = '当前用户无权查看用户列表'
        return
      }

      loading.value = true

      try {
        users.value = await getUsersApi()
      } catch (error) {
        errorMessage.value =
          error.userMessage || '用户列表加载失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(loadUsers)

    /* ==================== 本地搜索与状态筛选 ==================== */
    const keyword = ref('')
    const statusFilter = ref('all')

    const filteredUsers = computed(() => {
      const search = keyword.value.trim().toLowerCase()

      return users.value.filter((user) => {
        const matchesText =
          !search ||
          user.username.toLowerCase().includes(search) ||
          (user.email || '').toLowerCase().includes(search)

        const matchesStatus =
          statusFilter.value === 'all' ||
          (statusFilter.value === 'active' && user.is_active) ||
          (statusFilter.value === 'disabled' && !user.is_active)

        return matchesText && matchesStatus
      })
    })

    const activeCount = computed(
      () => users.value.filter((user) => user.is_active).length,
    )

    /* ==================== 列表展示辅助 ==================== */
    const formatTime = (value) => {
      if (!value) return '—'

      const date = new Date(value)
      return Number.isNaN(date.getTime())
        ? '—'
        : date.toLocaleString('zh-CN', { hour12: false })
    }

    /* ==================== 公共弹出层测试 ==================== */

    // 是否显示测试弹出层
    const modalTestVisible = ref(false)

    // 测试弹出层宽度
    const modalTestWidth = ref(560)

    const openModalTest = () => {
      modalTestVisible.value = true
    }

    const closeModalTest = () => {
      modalTestVisible.value = false
    }

    return {
      currentPage,
      parentPage,
      users,
      loading,
      errorMessage,
      loadUsers,
      keyword,
      statusFilter,
      filteredUsers,
      activeCount,
      formatTime,

      // 公共弹出层
      modalTestVisible,
      modalTestWidth,
      openModalTest,
      closeModalTest,
    }
  },
})