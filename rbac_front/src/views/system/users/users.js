/* ==================== Vue 相关依赖 ==================== */
import {
  computed,
  defineComponent,
  onMounted,
  reactive,
  ref,
} from 'vue'

/* ==================== 公共组件 ==================== */
import AppModal from '@/components/feedback/modal/app-modal.vue'
import AppSelect from '@/components/form/select/app-select.vue'

/* ==================== 用户与角色接口 ==================== */
import {
  assignUserRoleApi,
  createUserApi,
  getUserDetailApi,
  getUsersApi,
  updateUserApi,
  updateUserStatusApi,
} from '@/api/users'

import { getRolesApi } from '@/api/roles'

/* ==================== 状态与消息 ==================== */
import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

/* ==================== 表单初始值 ==================== */

const createInitialForm = () => {
  return {
    username: '',
    email: '',
    password: '',
    passwordConfirm: '',
    roleId: null,
    isActive: true,
  }
}

/* ==================== 固定下拉选项 ==================== */

/*
 * 用户状态筛选选项。
 */
const statusFilterOptions = [
  {
    label: '全部状态',
    value: 'all',
  },
  {
    label: '已启用',
    value: 'active',
  },
  {
    label: '已禁用',
    value: 'disabled',
  },
]

/*
 * 创建、编辑用户时使用的账号状态选项。
 *
 * value 保持 Boolean 类型，
 * 与 userForm.isActive 的数据类型一致。
 */
const userStatusOptions = [
  {
    label: '启用',
    value: true,
  },
  {
    label: '禁用',
    value: false,
  },
]

export default defineComponent({
  name: 'SystemUsers',

  /* ==================== 页面公共组件 ==================== */

  components: {
    AppModal,
    AppSelect,
  },

  setup() {
    const authStore = useAuthStore()

    /* ==================== 用户与角色数据 ==================== */

    const users = ref([])
    const roles = ref([])

    const loading = ref(false)
    const errorMessage = ref('')

    /* ==================== 当前用户操作权限 ==================== */

    /*
     * 根管理员会由 Auth Store 自动放行，
     * 这里不需要重复判断 is_root。
     */

    // 查看用户列表
    const canViewUserList = computed(() => {
      return authStore.hasPermission(
        'USER_LIST',
      )
    })

    // 查看用户详情
    const canViewUserDetail = computed(() => {
      return authStore.hasPermission(
        'USER_DETAIL',
      )
    })

    // 创建用户
    const canCreateUser = computed(() => {
      return authStore.hasPermission(
        'USER_CREATE',
      )
    })

    // 修改用户名和邮箱
    const canUpdateUser = computed(() => {
      return authStore.hasPermission(
        'USER_UPDATE',
      )
    })

    // 启用或停用用户
    const canChangeUserStatus = computed(() => {
      return authStore.hasPermission(
        'USER_CHANGE_STATUS',
      )
    })

    // 给用户分配或取消角色
    const canAssignUserRole = computed(() => {
      return authStore.hasPermission(
        'USER_ASSIGN_ROLE',
      )
    })

    // 重置普通用户密码
    const canResetUserPassword = computed(() => {
      return authStore.hasPermission(
        'USER_RESET_PASSWORD',
      )
    })

    /*
     * 编辑弹出层同时承担：
     *
     * 1. 修改基础资料；
     * 2. 分配用户角色。
     *
     * 拥有其中任意一个权限时，
     * 就可以显示编辑入口。
     */
    const canEditUser = computed(() => {
      return (
        canUpdateUser.value ||
        canAssignUserRole.value
      )
    })

    /*
     * 创建和编辑用户时，
     * 只允许选择当前处于启用状态的角色。
     */
    const activeRoles = computed(() => {
      return roles.value.filter((role) => {
        return role.is_active
      })
    })

    /* ==================== 角色下拉选项 ==================== */

    /*
     * 用户列表的角色筛选选项。
     *
     * 角色 ID 转换为字符串，
     * 与 roleFilter 当前使用的数据类型保持一致。
     */
    const roleFilterOptions = computed(() => {
      return [
        {
          label: '全部角色',
          value: 'all',
        },
        {
          label: '未分配角色',
          value: '',
        },
        ...roles.value.map((role) => {
          return {
            label: role.name,
            value: String(role.id),
            disabled: !role.is_active,
          }
        }),
      ]
    })

    /*
     * 创建和编辑用户时使用的角色选项。
     *
     * 未分配角色使用 null，
     * 角色 ID 保持 Number 类型，
     * 与后端接口需要的数据类型一致。
     */
    const userRoleOptions = computed(() => {
      return [
        {
          label: '暂不分配角色',
          value: null,
        },
        ...activeRoles.value.map((role) => {
          return {
            label: role.name,
            value: role.id,
          }
        }),
      ]
    })

    /* ==================== 加载用户列表 ==================== */

    const loadUsers = async () => {
      /*
       * 没有列表权限时，
       * 不发送必然返回403的请求。
       */
      if (!canViewUserList.value) {
        users.value = []
        errorMessage.value =
          '当前用户没有查看用户列表的权限'

        return
      }

      users.value = await getUsersApi()
    }

    /* ==================== 加载角色选项 ==================== */

    const loadRoles = async () => {
      /*
       * 获取完整角色列表需要 ROLE_LIST。
       *
       * 没有角色列表权限时不请求接口，
       * 避免用户管理页面整体因为403而无法加载。
       */
      if (
        !authStore.hasPermission('ROLE_LIST')
      ) {
        roles.value = []
        return
      }

      roles.value = await getRolesApi()
    }

    /* ==================== 初始化页面数据 ==================== */

    const loadPageData = async () => {
      errorMessage.value = ''
      loading.value = true

      try {
        await Promise.all([
          loadUsers(),
          loadRoles(),
        ])
      } catch (error) {
        errorMessage.value =
          error.userMessage ||
          '用户管理数据加载失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(loadPageData)

    /* ==================== 搜索与筛选 ==================== */

    const keyword = ref('')
    const roleFilter = ref('all')
    const statusFilter = ref('all')

    const filteredUsers = computed(() => {
      const search =
        keyword.value.trim().toLowerCase()

      return users.value.filter((user) => {
        /*
         * 搜索范围：
         * 用户名、邮箱和角色名称。
         */
        const searchContent = [
          user.username,
          user.email,
          user.role?.name,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()

        const matchesKeyword =
          !search ||
          searchContent.includes(search)

        const matchesRole =
          roleFilter.value === 'all' ||
          String(user.role?.id ?? '') ===
          String(roleFilter.value)

        const matchesStatus =
          statusFilter.value === 'all' ||
          (
            statusFilter.value === 'active' &&
            user.is_active
          ) ||
          (
            statusFilter.value === 'disabled' &&
            !user.is_active
          )

        return (
          matchesKeyword &&
          matchesRole &&
          matchesStatus
        )
      })
    })

    /* ==================== 用户统计 ==================== */

    const activeCount = computed(() => {
      return users.value.filter((user) => {
        return user.is_active
      }).length
    })

    const disabledCount = computed(() => {
      return users.value.length - activeCount.value
    })

    /* ==================== 显示模式 ==================== */

    /*
     * list：列表模式。
     * card：卡片模式。
     */
    const viewMode = ref('list')

    const setViewMode = (mode) => {
      if (!['list', 'card'].includes(mode)) {
        return
      }

      viewMode.value = mode
    }

    /* ==================== 展示辅助方法 ==================== */

    const getUserInitial = (user) => {
      return (
        user?.username
          ?.trim()
          .charAt(0)
          .toUpperCase() ||
        '用'
      )
    }

    const getUserRoleName = (user) => {
      if (user?.is_root) {
        return '根管理员'
      }

      return user?.role?.name || '未分配角色'
    }

    const formatTime = (value) => {
      if (!value) {
        return '—'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return '—'
      }

      return date.toLocaleString(
        'zh-CN',
        {
          hour12: false,
        },
      )
    }

    /* ==================== 后端错误解析 ==================== */

    const findFirstError = (errors) => {
      if (typeof errors === 'string') {
        return errors
      }

      if (Array.isArray(errors)) {
        for (const item of errors) {
          const result = findFirstError(item)

          if (result) {
            return result
          }
        }

        return ''
      }

      if (
        errors &&
        typeof errors === 'object'
      ) {
        for (
          const value of Object.values(errors)
        ) {
          const result = findFirstError(value)

          if (result) {
            return result
          }
        }
      }

      return ''
    }

    const getErrorMessage = (
      error,
      fallback,
    ) => {
      return (
        findFirstError(
          error.validationErrors,
        ) ||
        error.userMessage ||
        fallback
      )
    }

    /* ==================== 公共提交状态 ==================== */

    /*
     * 创建、编辑或修改状态时，
     * 禁止重复提交和关闭弹出层。
     */
    const submitting = ref(false)

    /* ==================== 用户表单状态 ==================== */

    /*
     * create：创建用户。
     * edit：编辑用户。
     */
    const formMode = ref('create')
    const formModalVisible = ref(false)
    const editingUser = ref(null)

    const userForm = reactive(
      createInitialForm(),
    )

    const isCreateMode = computed(() => {
      return formMode.value === 'create'
    })

    const formModalTitle = computed(() => {
      return isCreateMode.value
        ? '创建用户'
        : '编辑用户'
    })

    /* ==================== 重置用户表单 ==================== */

    const resetUserForm = () => {
      Object.assign(
        userForm,
        createInitialForm(),
      )

      editingUser.value = null
    }

    /* ==================== 打开创建弹出层 ==================== */

    const openCreateModal = () => {
      if (!canCreateUser.value) {
        message.warning(
          '当前用户没有创建用户的权限',
        )

        return
      }

      resetUserForm()

      formMode.value = 'create'
      formModalVisible.value = true
    }

    /* ==================== 打开编辑弹出层 ==================== */

    const openEditModal = (user) => {
      if (!canEditUser.value) {
        message.warning(
          '当前用户没有修改用户的权限',
        )

        return
      }

      if (!user) {
        return
      }

      resetUserForm()

      editingUser.value = user
      formMode.value = 'edit'

      userForm.username =
        user.username || ''

      userForm.email =
        user.email || ''

      userForm.roleId =
        user.role?.id ?? null

      userForm.isActive =
        Boolean(user.is_active)

      formModalVisible.value = true
    }

    /* ==================== 关闭用户表单 ==================== */

    const closeFormModal = () => {
      if (submitting.value) {
        return
      }

      formModalVisible.value = false
    }

    /* ==================== 用户表单验证 ==================== */

    const validateUserForm = () => {
      const username =
        userForm.username.trim()

      if (!username) {
        message.warning('请输入用户名')
        return false
      }

      if (
        username.length < 4 ||
        username.length > 20
      ) {
        message.warning(
          '用户名长度必须为 4～20 个字符',
        )

        return false
      }

      if (/\s/.test(username)) {
        message.warning(
          '用户名不能包含空白字符',
        )

        return false
      }

      if (isCreateMode.value) {
        if (!userForm.password) {
          message.warning('请输入密码')
          return false
        }

        if (/\s/.test(userForm.password)) {
          message.warning(
            '密码不能包含空白字符',
          )

          return false
        }

        if (
          userForm.password !==
          userForm.passwordConfirm
        ) {
          message.warning(
            '两次输入的密码不一致',
          )

          return false
        }
      }

      return true
    }

    /* ==================== 创建用户 ==================== */

    const createUser = async () => {
      /*
       * 第一步：创建基础用户。
       */
      const createdUser =
        await createUserApi({
          username:
            userForm.username.trim(),
          email:
            userForm.email.trim() || null,
          password:
            userForm.password,
          password_confirm:
            userForm.passwordConfirm,
        })

      const followUpErrors = []

      /*
       * 第二步：分配角色。
       *
       * 用户没有选择角色时保持 role = null。
       */
      if (canAssignUserRole.value && userForm.roleId != null) {
        try {
          await assignUserRoleApi(
            createdUser.id,
            userForm.roleId,
          )
        } catch (error) {
          followUpErrors.push(
            '角色分配失败',
          )
        }
      }

      /*
       * 第三步：创建接口默认启用账号。
       *
       * 如果管理员选择停用状态，
       * 创建完成后再单独修改状态。
       */
      if (canChangeUserStatus.value && !userForm.isActive) {
        try {
          await updateUserStatusApi(
            createdUser.id,
            false,
          )
        } catch (error) {
          followUpErrors.push(
            '账号状态设置失败',
          )
        }
      }

      await loadUsers()

      formModalVisible.value = false

      if (followUpErrors.length) {
        message.warning(
          `用户已创建，但${followUpErrors.join('、')}`,
        )

        return
      }

      message.success('用户创建成功')
    }

    /* ==================== 编辑用户 ==================== */

    const updateUser = async () => {
      if (!editingUser.value) {
        return
      }

      const userId =
        editingUser.value.id

      const followUpErrors = []

      /*
       * 拥有 USER_UPDATE 时，
       * 才修改用户名和邮箱。
       */
      if (canUpdateUser.value) {
        try {
          await updateUserApi(
            userId,
            {
              username:
                userForm.username.trim(),
              email:
                userForm.email.trim() || null,
            },
          )
        } catch (error) {
          followUpErrors.push(
            getErrorMessage(
              error,
              '用户资料修改失败',
            ),
          )
        }
      }

      /*
       * 拥有 USER_ASSIGN_ROLE 时，
       * 才检查和修改用户角色。
       */
      if (canAssignUserRole.value) {
        const oldRoleId =
          editingUser.value.role?.id ?? null

        const newRoleId =
          userForm.roleId ?? null

        if (
          String(oldRoleId) !==
          String(newRoleId)
        ) {
          try {
            await assignUserRoleApi(
              userId,
              newRoleId,
            )
          } catch (error) {
            followUpErrors.push(
              getErrorMessage(
                error,
                '用户角色修改失败',
              ),
            )
          }
        }
      }

      await loadUsers()

      /*
       * 有任意操作失败时保留弹出层，
       * 方便管理员检查后重新提交。
       */
      if (followUpErrors.length) {
        message.warning(
          followUpErrors.join('；'),
        )

        return
      }

      formModalVisible.value = false

      message.success('用户信息修改成功')
    }

    /* ==================== 提交用户表单 ==================== */

    const submitUserForm = async () => {
      if (
        submitting.value ||
        !validateUserForm()
      ) {
        return
      }

      submitting.value = true

      try {
        if (isCreateMode.value) {
          await createUser()
        } else {
          await updateUser()
        }
      } catch (error) {
        message.error(
          getErrorMessage(
            error,
            isCreateMode.value
              ? '用户创建失败'
              : '用户修改失败',
          ),
        )
      } finally {
        submitting.value = false
      }
    }

    /* ==================== 用户详情弹出层 ==================== */

    const detailModalVisible = ref(false)
    const detailLoading = ref(false)
    const selectedUser = ref(null)

    const openDetailModal = async (user) => {
      if (!canViewUserDetail.value) {
        message.warning(
          '当前用户没有查看用户详情的权限',
        )

        return
      }

      if (!user || detailLoading.value) {
        return
      }

      detailModalVisible.value = true
      detailLoading.value = true
      selectedUser.value = null

      try {
        selectedUser.value =
          await getUserDetailApi(user.id)
      } catch (error) {
        detailModalVisible.value = false

        message.error(
          getErrorMessage(
            error,
            '用户信息加载失败',
          ),
        )
      } finally {
        detailLoading.value = false
      }
    }

    const closeDetailModal = () => {
      if (detailLoading.value) {
        return
      }

      detailModalVisible.value = false
    }

    /*
     * 从详情弹出层进入编辑弹出层。
     */
    const editSelectedUser = () => {
      if (!selectedUser.value) {
        return
      }

      detailModalVisible.value = false
      openEditModal(selectedUser.value)
    }

    /* ==================== 状态确认弹出层 ==================== */

    const statusModalVisible = ref(false)
    const statusTargetUser = ref(null)

    const openStatusModal = (user) => {
      if (!canChangeUserStatus.value) {
        message.warning(
          '当前用户没有修改用户状态的权限',
        )

        return
      }

      if (!user) {
        return
      }

      /*
       * 后端不允许禁用根管理员。
       */
      if (
        user.is_root &&
        user.is_active
      ) {
        message.warning(
          '不能禁用根管理员账号',
        )

        return
      }

      statusTargetUser.value = user
      statusModalVisible.value = true
    }

    const closeStatusModal = () => {
      if (submitting.value) {
        return
      }

      statusModalVisible.value = false
    }

    const statusModalTitle = computed(() => {
      if (
        statusTargetUser.value?.is_active
      ) {
        return '禁用用户'
      }

      return '启用用户'
    })

    const statusActionText = computed(() => {
      if (
        statusTargetUser.value?.is_active
      ) {
        return '确认禁用'
      }

      return '确认启用'
    })

    const confirmUserStatus = async () => {
      if (
        submitting.value ||
        !statusTargetUser.value
      ) {
        return
      }

      submitting.value = true

      const target =
        statusTargetUser.value

      const newStatus =
        !target.is_active

      try {
        await updateUserStatusApi(
          target.id,
          newStatus,
        )

        await loadUsers()

        statusModalVisible.value = false

        message.success(
          newStatus
            ? '用户已启用'
            : '用户已禁用',
        )
      } catch (error) {
        message.error(
          getErrorMessage(
            error,
            newStatus
              ? '用户启用失败'
              : '用户禁用失败',
          ),
        )
      } finally {
        submitting.value = false
      }
    }

    /* ==================== 向模板暴露内容 ==================== */

    return {

      /* ==================== 操作权限 ==================== */

      canViewUserList,
      canViewUserDetail,
      canCreateUser,
      canUpdateUser,
      canChangeUserStatus,
      canAssignUserRole,
      canResetUserPassword,
      canEditUser,

      users,
      roles,
      activeRoles,
      loading,
      errorMessage,

      roleFilterOptions,
      statusFilterOptions,
      userRoleOptions,
      userStatusOptions,

      keyword,
      roleFilter,
      statusFilter,
      filteredUsers,

      activeCount,
      disabledCount,

      viewMode,
      setViewMode,

      getUserInitial,
      getUserRoleName,
      formatTime,

      submitting,

      formMode,
      formModalVisible,
      formModalTitle,
      isCreateMode,
      userForm,
      openCreateModal,
      openEditModal,
      closeFormModal,
      submitUserForm,

      detailModalVisible,
      detailLoading,
      selectedUser,
      openDetailModal,
      closeDetailModal,
      editSelectedUser,

      statusModalVisible,
      statusTargetUser,
      statusModalTitle,
      statusActionText,
      openStatusModal,
      closeStatusModal,
      confirmUserStatus,

      loadPageData,
    }
  },
})