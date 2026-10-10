/* ==================== Vue 与路由 ==================== */

import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

/* ==================== 系统概览接口 ==================== */

import { getSystemOverviewApi } from '@/api/dashboard'

/* ==================== 初始概览数据 ==================== */

const createInitialOverview = () => ({
  users: {
    total: 0,
    active: 0,
    status: { normal: 0, new: 0, disabled: 0 },
  },
  roles: { total: 0, active: 0 },
  pages: { total: 0, active: 0, top_level: 0, disabled: 0 },
  role_distribution: { items: [], unassigned_user_count: 0 },
  recent_users: [],
})

export default defineComponent({
  name: 'SystemDashboard',

  setup() {
    /* ==================== 路由与页面状态 ==================== */

    const router = useRouter()
    const overview = ref(createInitialOverview())
    const loading = ref(false)
    const errorMessage = ref('')
    const updatedAt = ref(null)

    /* ==================== 数据格式化 ==================== */

    const formatNumber = (value) => {
      const number = Number(value)

      return Number.isFinite(number)
        ? number.toLocaleString('zh-CN')
        : '0'
    }

    const formatUpdatedAt = computed(() => {
      if (!updatedAt.value) return '尚未更新'

      return new Intl.DateTimeFormat('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
      }).format(updatedAt.value)
    })

    const getUserInitial = (user) => {
      return user?.username?.trim().charAt(0).toUpperCase() || '用'
    }

    /* ==================== 用户状态统计 ==================== */

    const userStatuses = computed(() => {
      const status = overview.value.users?.status || {}

      return [
        {
          key: 'normal',
          label: '正常用户',
          value: Number(status.normal) || 0,
          colorClass: 'blue',
        },
        {
          key: 'new',
          label: '新增用户',
          value: Number(status.new) || 0,
          colorClass: 'green',
        },
        {
          key: 'disabled',
          label: '已禁用',
          value: Number(status.disabled) || 0,
          colorClass: 'gray',
        },
      ]
    })

    const statusTotal = computed(() => {
      return userStatuses.value.reduce(
        (total, item) => total + item.value,
        0,
      )
    })

    const getStatusPercentage = (value) => {
      if (statusTotal.value <= 0) return 0

      return Math.round((value / statusTotal.value) * 100)
    }

    const donutStyle = computed(() => {
      if (statusTotal.value <= 0) {
        return { background: 'var(--border)' }
      }

      const normalEnd = getStatusPercentage(userStatuses.value[0].value)
      const newEnd = Math.min(
        normalEnd + getStatusPercentage(userStatuses.value[1].value),
        100,
      )

      return {
        background: `conic-gradient(
          var(--primary) 0 ${normalEnd}%,
          var(--success) ${normalEnd}% ${newEnd}%,
          var(--text-muted) ${newEnd}% 100%
        )`,
      }
    })

    /* ==================== 角色分布 ==================== */

    const roleDistribution = computed(() => {
      const distribution = overview.value.role_distribution || {}
      const roles = Array.isArray(distribution.items)
        ? distribution.items
        : []

      const items = roles.map((role) => ({
        id: role.id,
        name: role.name || '未命名角色',
        code: role.code || '—',
        userCount: Number(role.user_count) || 0,
        unassigned: false,
      }))

      const unassignedCount = Number(distribution.unassigned_user_count) || 0

      if (unassignedCount > 0) {
        items.push({
          id: 'unassigned',
          name: '未分配角色',
          code: 'UNASSIGNED',
          userCount: unassignedCount,
          unassigned: true,
        })
      }

      return items
    })

    /* ==================== 页面跳转 ==================== */

    const navigateTo = (routeName) => {
      router.push({ name: routeName })
    }

    /* ==================== 加载系统概览 ==================== */

    const loadOverview = async () => {
      if (loading.value) return

      loading.value = true
      errorMessage.value = ''

      try {
        const data = await getSystemOverviewApi()
        const initial = createInitialOverview()

        overview.value = {
          ...initial,
          ...data,
          users: {
            ...initial.users,
            ...data?.users,
            status: {
              ...initial.users.status,
              ...data?.users?.status,
            },
          },
          roles: { ...initial.roles, ...data?.roles },
          pages: { ...initial.pages, ...data?.pages },
          role_distribution: {
            ...initial.role_distribution,
            ...data?.role_distribution,
          },
          recent_users: Array.isArray(data?.recent_users)
            ? data.recent_users
            : [],
        }

        updatedAt.value = new Date()
      } catch (error) {
        errorMessage.value =
          error.userMessage || '系统概览加载失败，请稍后重试'
      } finally {
        loading.value = false
      }
    }

    /* ==================== 页面初始化 ==================== */

    onMounted(loadOverview)

    /* ==================== 向模板暴露内容 ==================== */

    return {
      overview,
      loading,
      errorMessage,
      formatUpdatedAt,
      userStatuses,
      donutStyle,
      roleDistribution,
      formatNumber,
      getUserInitial,
      getStatusPercentage,
      navigateTo,
      loadOverview,
    }
  },
})
