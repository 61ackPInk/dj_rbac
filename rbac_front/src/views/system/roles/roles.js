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

/* ==================== 角色接口 ==================== */

import {
  createRoleApi,
  getRoleDetailApi,
  getRolesApi,
  updateRoleApi,
  updateRoleStatusApi,
  getRolePermissionsApi,
  updateRolePermissionsApi,
} from '@/api/roles'

/* ==================== 权限与页面接口 ==================== */

import {
  getPermissionsApi,
} from '@/api/permissions'

import {
  getPagesApi,
} from '@/api/pages'

/* ==================== 状态与消息 ==================== */

import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

/* ==================== 角色表单初始值 ==================== */

const createInitialForm = () => {
  return {
    name: '',
    code: '',
    rank: 1,
    description: '',
    isActive: true,
  }
}

/* ==================== 固定下拉选项 ==================== */

/*
 * 角色列表状态筛选。
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
    label: '已停用',
    value: 'disabled',
  },
]

/*
 * 创建、编辑角色时使用的状态选项。
 */
const roleStatusOptions = [
  {
    label: '启用',
    value: true,
  },
  {
    label: '停用',
    value: false,
  },
]

/* ==================== 角色管理页面 ==================== */

export default defineComponent({
  name: 'SystemRoles',

  /* ==================== 页面公共组件 ==================== */

  components: {
    AppModal,
    AppSelect,
  },

  setup() {
    const authStore = useAuthStore()

    /* ==================== 当前用户操作权限 ==================== */

    /*
     * 角色管理中的每项操作使用独立权限。
     *
     * 根管理员会在 Auth Store 中自动放行，
     * 因此这里不需要重复判断 is_root。
     */

    // 查看角色列表
    const canViewRoleList = computed(() => {
      return authStore.hasPermission(
        'ROLE_LIST',
      )
    })

    // 查看角色详情
    const canViewRoleDetail = computed(() => {
      return authStore.hasPermission(
        'ROLE_DETAIL',
      )
    })

    // 创建角色
    const canCreateRole = computed(() => {
      return authStore.hasPermission(
        'ROLE_CREATE',
      )
    })

    // 修改角色资料
    const canUpdateRole = computed(() => {
      return authStore.hasPermission(
        'ROLE_UPDATE',
      )
    })

    // 启用或停用角色
    const canChangeRoleStatus = computed(() => {
      return authStore.hasPermission(
        'ROLE_CHANGE_STATUS',
      )
    })

    /* ==================== 高风险权限配置 ==================== */

    /*
     * 给角色配置操作权限只允许根管理员。
     *
     * 这里不能使用 ROLE_UPDATE 判断，
     * 因为普通角色管理员不能给自己或其他角色提权。
     */
    const canConfigureRolePermissions = computed(() => {
      return Boolean(authStore.isRoot)
    })

    /* ==================== 角色数据 ==================== */

    const roles = ref([])
    const loading = ref(false)
    const errorMessage = ref('')

    /* ==================== 加载角色列表 ==================== */

    const loadRoles = async () => {
      errorMessage.value = ''

      /*
       * 没有角色列表权限时，
       * 不发送必然返回403的请求。
       */
      if (!canViewRoleList.value) {
        roles.value = []
        errorMessage.value =
          '当前用户没有查看角色列表的权限'

        return
      }

      loading.value = true

      try {
        roles.value = await getRolesApi()
      } catch (error) {
        roles.value = []

        errorMessage.value =
          error.userMessage ||
          '角色列表加载失败'
      } finally {
        loading.value = false
      }
    }

    /* ==================== 页面初始化 ==================== */

    onMounted(() => {
      loadRoles()
    })

    onMounted(loadRoles)

    /* ==================== 搜索与筛选 ==================== */

    const keyword = ref('')
    const statusFilter = ref('all')

    const filteredRoles = computed(() => {
      const search =
        keyword.value.trim().toLowerCase()

      return roles.value.filter((role) => {
        /*
         * 搜索范围：
         * 角色名称、角色编码和角色描述。
         */
        const searchContent = [
          role.name,
          role.code,
          role.description,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()

        const matchesKeyword =
          !search ||
          searchContent.includes(search)

        const matchesStatus =
          statusFilter.value === 'all' ||
          (
            statusFilter.value === 'active' &&
            role.is_active
          ) ||
          (
            statusFilter.value === 'disabled' &&
            !role.is_active
          )

        return (
          matchesKeyword &&
          matchesStatus
        )
      })
    })

    /* ==================== 角色统计 ==================== */

    const activeCount = computed(() => {
      return roles.value.filter((role) => {
        return role.is_active
      }).length
    })

    const disabledCount = computed(() => {
      return roles.value.length -
        activeCount.value
    })

    /* ==================== 显示模式 ==================== */

    /*
     * list：列表显示。
     * card：卡片显示。
     */
    const viewMode = ref('list')

    const setViewMode = (mode) => {
      if (!['list', 'card'].includes(mode)) {
        return
      }

      viewMode.value = mode
    }

    /* ==================== 展示辅助方法 ==================== */

    /*
     * 生成角色头像文字。
     *
     * 优先使用角色编码的第一个字符，
     * 没有编码时使用角色名称。
     */
    const getRoleInitial = (role) => {
      return (
        role?.code
          ?.trim()
          .charAt(0)
          .toUpperCase() ||
        role?.name
          ?.trim()
          .charAt(0)
          .toUpperCase() ||
        '角'
      )
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
          const result =
            findFirstError(item)

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
          const value of Object.values(
            errors,
          )
        ) {
          const result =
            findFirstError(value)

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
     * 创建、编辑、启用或停用角色时，
     * 防止重复提交和误关弹出层。
     */
    const submitting = ref(false)

    /* ==================== 角色表单状态 ==================== */

    /*
     * create：创建角色。
     * edit：编辑角色。
     */
    const formMode = ref('create')
    const formModalVisible = ref(false)
    const editingRole = ref(null)

    const roleForm = reactive(
      createInitialForm(),
    )

    const isCreateMode = computed(() => {
      return formMode.value === 'create'
    })

    const formModalTitle = computed(() => {
      return isCreateMode.value
        ? '创建角色'
        : '编辑角色'
    })

    /* ==================== 重置角色表单 ==================== */

    const resetRoleForm = () => {
      Object.assign(
        roleForm,
        createInitialForm(),
      )

      editingRole.value = null
    }

    /* ==================== 打开创建弹出层 ==================== */

    const openCreateModal = () => {
      if (!canCreateRole.value) {
        message.warning(
          '当前用户没有创建角色的权限',
        )

        return
      }

      resetRoleForm()

      formMode.value = 'create'
      formModalVisible.value = true
    }

    /* ==================== 打开编辑弹出层 ==================== */

    const openEditModal = (role) => {
      if (!canUpdateRole.value) {
        message.warning(
          '当前用户没有修改角色的权限',
        )

        return
      }

      if (!role) {
        return
      }

      resetRoleForm()

      editingRole.value = role
      formMode.value = 'edit'

      roleForm.name = role.name || ''
      roleForm.code = role.code || ''
      roleForm.rank =
        Number(role.rank) || 1
      roleForm.description =
        role.description || ''
      roleForm.isActive =
        Boolean(role.is_active)

      formModalVisible.value = true
    }

    /* ==================== 关闭角色表单 ==================== */

    const closeFormModal = () => {
      if (submitting.value) {
        return
      }

      formModalVisible.value = false
    }

    /* ==================== 规范化角色编码 ==================== */

    const normalizeRoleCode = () => {
      roleForm.code =
        roleForm.code
          .trim()
          .toUpperCase()
    }

    /* ==================== 角色表单验证 ==================== */

    const validateRoleForm = () => {
      const name =
        roleForm.name.trim()

      const code =
        roleForm.code.trim().toUpperCase()

      const rank =
        Number(roleForm.rank)

      if (!name) {
        message.warning('请输入角色名称')
        return false
      }

      if (
        name.length < 2 ||
        name.length > 50
      ) {
        message.warning(
          '角色名称长度必须为 2～50 个字符',
        )

        return false
      }

      if (!code) {
        message.warning('请输入角色编码')
        return false
      }

      /*
       * 后端规则：
       * 必须以字母开头，
       * 只能包含字母、数字和下划线。
       */
      if (
        !/^[A-Za-z][A-Za-z0-9_]*$/.test(
          code,
        )
      ) {
        message.warning(
          '角色编码必须以字母开头，且只能包含字母、数字和下划线',
        )

        return false
      }

      if (code.length > 50) {
        message.warning(
          '角色编码不能超过50个字符',
        )

        return false
      }

      if (
        !Number.isInteger(rank) ||
        rank < 1
      ) {
        message.warning(
          '角色权重必须是大于0的整数',
        )

        return false
      }

      if (
        roleForm.description.length > 255
      ) {
        message.warning(
          '角色描述不能超过255个字符',
        )

        return false
      }

      /*
       * 验证成功后统一整理数据。
       */
      roleForm.name = name
      roleForm.code = code
      roleForm.rank = rank
      roleForm.description =
        roleForm.description.trim()

      return true
    }

    /* ==================== 创建角色 ==================== */

    const createRole = async () => {
      await createRoleApi({
        name: roleForm.name,
        code: roleForm.code,
        rank: roleForm.rank,
        description:
          roleForm.description,
        is_active:
          roleForm.isActive,
      })

      await loadRoles()

      formModalVisible.value = false

      message.success('角色创建成功')
    }

    /* ==================== 编辑角色 ==================== */

    const updateRole = async () => {
      if (!editingRole.value) {
        return
      }

      /*
      * 角色资料接口不能修改状态。
      *
      * 状态必须通过：
      * PATCH /roles/{id}/status/
      * 单独修改。
      */
      await updateRoleApi(
        editingRole.value.id,
        {
          name: roleForm.name,
          code: roleForm.code,
          rank: roleForm.rank,
          description:
            roleForm.description,
        },
      )

      await loadRoles()

      formModalVisible.value = false

      message.success('角色信息修改成功')
    }

    /* ==================== 提交角色表单 ==================== */

    const submitRoleForm = async () => {
      if (
        submitting.value ||
        !validateRoleForm()
      ) {
        return
      }

      submitting.value = true

      try {
        if (isCreateMode.value) {
          await createRole()
        } else {
          await updateRole()
        }
      } catch (error) {
        message.error(
          getErrorMessage(
            error,
            isCreateMode.value
              ? '角色创建失败'
              : '角色修改失败',
          ),
        )
      } finally {
        submitting.value = false
      }
    }

    /* ==================== 角色详情弹出层 ==================== */

    const detailModalVisible = ref(false)
    const detailLoading = ref(false)
    const selectedRole = ref(null)

    const openDetailModal = async (role) => {
      if (!canViewRoleDetail.value) {
        message.warning(
          '当前用户没有查看角色详情的权限',
        )

        return
      }

      if (!role || detailLoading.value) {
        return
      }

      detailModalVisible.value = true
      detailLoading.value = true
      selectedRole.value = null

      try {
        selectedRole.value =
          await getRoleDetailApi(role.id)
      } catch (error) {
        detailModalVisible.value = false

        message.error(
          getErrorMessage(
            error,
            '角色信息加载失败',
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
     * 从角色详情直接进入编辑。
     */
    const editSelectedRole = () => {
      if (!selectedRole.value) {
        return
      }

      detailModalVisible.value = false
      openEditModal(selectedRole.value)
    }

    /* ==================== 角色权限配置弹出层 ==================== */

    /*
     * 当前正在配置权限的角色。
     */
    const permissionTargetRole = ref(null)

    /*
     * 权限配置弹出层状态。
     */
    const permissionModalVisible = ref(false)
    const permissionLoading = ref(false)
    const permissionSaving = ref(false)

    /*
     * 后端返回的全部权限定义。
     */
    const permissionDefinitions = ref([])

    /*
     * 系统中的页面数据。
     *
     * 页面响应中包含 visible_roles，
     * 可以判断当前角色拥有哪些页面。
     */
    const permissionPages = ref([])

    /*
     * 当前角色已经选中的权限 ID。
     */
    const selectedPermissionIds = ref([])

    /* ==================== 当前角色拥有的页面 ==================== */

    /*
     * 角色只能获得自己可见页面下的操作权限。
     *
     * 页面与角色关系来自：
     * page.visible_roles
     */
    const roleVisiblePageIds = computed(() => {
      const roleId =
        permissionTargetRole.value?.id

      if (!roleId) {
        return []
      }

      return permissionPages.value
        .filter((page) => {
          if (!page.is_active) {
            return false
          }

          return (
            page.visible_roles || []
          ).some((role) => {
            return role.id === roleId
          })
        })
        .map((page) => page.id)
    })

    /* ==================== 按页面分组权限 ==================== */

    /*
     * 只显示以下权限：
     *
     * 1. 权限本身处于启用状态；
     * 2. 权限所属页面处于启用状态；
     * 3. 当前角色已经拥有该页面。
     */
    const permissionGroups = computed(() => {
      const visiblePageIdSet = new Set(
        roleVisiblePageIds.value,
      )

      const groupMap = new Map()

      permissionDefinitions.value
        .filter((permission) => {
          return (
            permission.is_active &&
            permission.page &&
            visiblePageIdSet.has(
              permission.page.id,
            )
          )
        })
        .forEach((permission) => {
          const pageId = permission.page.id

          if (!groupMap.has(pageId)) {
            groupMap.set(pageId, {
              pageId,
              pageName:
                permission.page.name,
              pageCode:
                permission.page.code,
              permissions: [],
            })
          }

          groupMap
            .get(pageId)
            .permissions.push(permission)
        })

      return Array.from(
        groupMap.values(),
      )
    })

    /* ==================== 权限选择判断 ==================== */

    const isPermissionChecked = (
      permissionId,
    ) => {
      return selectedPermissionIds.value.includes(
        permissionId,
      )
    }

    /*
     * 判断某个页面中的权限是否已经全部选中。
     */
    const isPermissionGroupChecked = (
      group,
    ) => {
      if (!group.permissions.length) {
        return false
      }

      return group.permissions.every(
        (permission) => {
          return isPermissionChecked(
            permission.id,
          )
        },
      )
    }

    /*
     * 判断页面权限是否处于部分选中状态。
     */
    const isPermissionGroupIndeterminate = (
      group,
    ) => {
      const checkedCount =
        group.permissions.filter(
          (permission) => {
            return isPermissionChecked(
              permission.id,
            )
          },
        ).length

      return (
        checkedCount > 0 &&
        checkedCount <
        group.permissions.length
      )
    }

    /* ==================== 切换单个操作权限 ==================== */

    const togglePermission = (
      permissionId,
      checked,
    ) => {
      const permissionIdSet = new Set(
        selectedPermissionIds.value,
      )

      if (checked) {
        permissionIdSet.add(permissionId)
      } else {
        permissionIdSet.delete(permissionId)
      }

      selectedPermissionIds.value =
        Array.from(permissionIdSet)
    }

    /* ==================== 切换页面全部权限 ==================== */

    const togglePermissionGroup = (
      group,
      checked,
    ) => {
      const permissionIdSet = new Set(
        selectedPermissionIds.value,
      )

      group.permissions.forEach(
        (permission) => {
          if (checked) {
            permissionIdSet.add(
              permission.id,
            )
          } else {
            permissionIdSet.delete(
              permission.id,
            )
          }
        },
      )

      selectedPermissionIds.value =
        Array.from(permissionIdSet)
    }

    /* ==================== 打开权限配置弹出层 ==================== */

    const openPermissionModal = async (role) => {
      if (!canConfigureRolePermissions.value) {
        message.warning(
          '只有根管理员可以配置角色权限',
        )

        return
      }

      if (
        !role ||
        permissionLoading.value
      ) {
        return
      }

      permissionTargetRole.value = role
      permissionDefinitions.value = []
      permissionPages.value = []
      selectedPermissionIds.value = []

      permissionModalVisible.value = true
      permissionLoading.value = true

      try {
        /*
         * 同时加载：
         *
         * 1. 系统全部权限定义；
         * 2. 当前角色已有权限；
         * 3. 页面与可见角色关系。
         */
        const [
          permissions,
          roleDetail,
          pages,
        ] = await Promise.all([
          getPermissionsApi(),
          getRolePermissionsApi(role.id),
          getPagesApi(),
        ])

        permissionDefinitions.value =
          Array.isArray(permissions)
            ? permissions
            : []

        permissionPages.value =
          Array.isArray(pages)
            ? pages
            : []

        selectedPermissionIds.value =
          (
            roleDetail.permissions || []
          ).map((permission) => {
            return permission.id
          })
      } catch (error) {
        permissionModalVisible.value = false

        message.error(
          getErrorMessage(
            error,
            '角色权限加载失败',
          ),
        )
      } finally {
        permissionLoading.value = false
      }
    }

    /* ==================== 关闭权限配置弹出层 ==================== */

    const closePermissionModal = () => {
      if (
        permissionLoading.value ||
        permissionSaving.value
      ) {
        return
      }

      permissionModalVisible.value = false
    }

    /* ==================== 保存角色操作权限 ==================== */

    const saveRolePermissions = async () => {
      if (
        !permissionTargetRole.value ||
        permissionLoading.value ||
        permissionSaving.value
      ) {
        return
      }

      permissionSaving.value = true

      try {
        await updateRolePermissionsApi(
          permissionTargetRole.value.id,
          selectedPermissionIds.value,
        )

        await loadRoles()

        permissionModalVisible.value = false

        message.success(
          '角色操作权限配置成功',
        )
      } catch (error) {
        message.error(
          getErrorMessage(
            error,
            '角色操作权限配置失败',
          ),
        )
      } finally {
        permissionSaving.value = false
      }
    }

    /* ==================== 状态确认弹出层 ==================== */

    const statusModalVisible = ref(false)
    const statusTargetRole = ref(null)

    const openStatusModal = (role) => {
      if (!canChangeRoleStatus.value) {
        message.warning(
          '当前用户没有修改角色状态的权限',
        )

        return
      }

      if (!role) {
        return
      }

      statusTargetRole.value = role
      statusModalVisible.value = true
    }

    const closeStatusModal = () => {
      if (submitting.value) {
        return
      }

      statusModalVisible.value = false
    }

    const statusModalTitle = computed(() => {
      return statusTargetRole.value
        ?.is_active
        ? '停用角色'
        : '启用角色'
    })

    const statusActionText = computed(() => {
      return statusTargetRole.value
        ?.is_active
        ? '确认停用'
        : '确认启用'
    })

    const confirmRoleStatus = async () => {
      if (
        submitting.value ||
        !statusTargetRole.value
      ) {
        return
      }

      submitting.value = true

      const target =
        statusTargetRole.value

      const shouldEnable =
        !target.is_active

      try {
        /*
         * 新版后端使用统一状态接口：
         *
         * PATCH /roles/{id}/status/
         * {
         *   is_active: true 或 false
         * }
         */
        await updateRoleStatusApi(
          target.id,
          shouldEnable,
        )

        await loadRoles()

        statusModalVisible.value = false

        message.success(
          shouldEnable
            ? '角色已启用'
            : '角色已停用',
        )
      } catch (error) {
        message.error(
          getErrorMessage(
            error,
            shouldEnable
              ? '角色启用失败'
              : '角色停用失败',
          ),
        )
      } finally {
        submitting.value = false
      }
    }

    /* ==================== 向模板暴露内容 ==================== */

    return {
      /* ==================== 操作权限 ==================== */

      canViewRoleList,
      canViewRoleDetail,
      canCreateRole,
      canUpdateRole,
      canChangeRoleStatus,
      canConfigureRolePermissions,

      roles,
      loading,
      errorMessage,
      loadRoles,

      keyword,
      statusFilter,
      statusFilterOptions,
      filteredRoles,

      activeCount,
      disabledCount,

      viewMode,
      setViewMode,

      getRoleInitial,
      formatTime,

      submitting,

      formMode,
      formModalVisible,
      formModalTitle,
      isCreateMode,
      roleForm,
      roleStatusOptions,
      openCreateModal,
      openEditModal,
      closeFormModal,
      normalizeRoleCode,
      submitRoleForm,

      detailModalVisible,
      detailLoading,
      selectedRole,
      openDetailModal,
      closeDetailModal,
      editSelectedRole,

      statusModalVisible,
      statusTargetRole,
      statusModalTitle,
      statusActionText,
      openStatusModal,
      closeStatusModal,
      confirmRoleStatus,

      /* ==================== 角色权限配置 ==================== */

      permissionTargetRole,
      permissionModalVisible,
      permissionLoading,
      permissionSaving,
      permissionGroups,
      selectedPermissionIds,

      isPermissionChecked,
      isPermissionGroupChecked,
      isPermissionGroupIndeterminate,
      togglePermission,
      togglePermissionGroup,

      openPermissionModal,
      closePermissionModal,
      saveRolePermissions,
    }
  },
})