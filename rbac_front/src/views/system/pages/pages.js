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
import AppActionMenu from '@/components/common/action-menu/action-menu.vue'

/* ==================== 页面与角色接口 ==================== */

import {
    createPageApi,
    getPageDetailApi,
    getPagesApi,
    updatePageApi,
    updatePageRolesApi,
    updatePageStatusApi,
} from '@/api/pages'

import {
    getRolesApi,
} from '@/api/roles'

/* ==================== 图标配置 ==================== */

import {
    DEFAULT_PAGE_ICON,
    bootstrapIconOptions,
} from '@/constants/bootstrap-icons'

/* ==================== 状态管理与消息 ==================== */

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'
import { message } from '@/utils/message'

/* ==================== 页面表单初始值 ==================== */

const createInitialForm = () => {
    return {
        name: '',
        code: '',
        path: '',
        component: '',
        icon: DEFAULT_PAGE_ICON,
        parentId: null,
        visibleRoleIds: [],
        sortOrder: 0,
        isActive: true,
    }
}

/* ==================== 固定下拉选项 ==================== */

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

const pageStatusOptions = [
    {
        label: '启用',
        value: true,
    },
    {
        label: '停用',
        value: false,
    },
]

/* ==================== 页面管理视图 ==================== */

export default defineComponent({
    name: 'SystemPages',

    /* ==================== 页面公共组件 ==================== */

    components: {
        AppModal,
        AppSelect,
        AppActionMenu,
    },

    setup() {
        const authStore = useAuthStore()
        const navigationStore =
            useNavigationStore()

        /* ==================== 当前用户操作权限 ==================== */

        // 查看页面列表
        const canViewPageList = computed(() => {
            return authStore.hasPermission(
                'PAGE_LIST',
            )
        })

        // 查看页面详情
        const canViewPageDetail = computed(() => {
            return authStore.hasPermission(
                'PAGE_DETAIL',
            )
        })

        // 创建页面
        const canCreatePage = computed(() => {
            return authStore.hasPermission(
                'PAGE_CREATE',
            )
        })

        // 修改页面基础资料
        const canUpdatePage = computed(() => {
            return authStore.hasPermission(
                'PAGE_UPDATE',
            )
        })

        // 启用或停用页面
        const canChangePageStatus = computed(() => {
            return authStore.hasPermission(
                'PAGE_CHANGE_STATUS',
            )
        })

        // 配置页面可见角色
        const canAssignPageRole = computed(() => {
            return authStore.hasPermission(
                'PAGE_ASSIGN_ROLE',
            )
        })

        /*
         * 编辑弹出层包含：
         *
         * 1. 页面基础资料；
         * 2. 页面可见角色。
         *
         * 拥有其中任意权限即可打开。
         */
        const canEditPage = computed(() => {
            return (
                canUpdatePage.value ||
                canAssignPageRole.value
            )
        })

        /* ==================== 页面行操作菜单 ==================== */

        /* 是否至少拥有一项页面操作权限 */
        const hasPageActions = computed(() => {
            return (
                canViewPageDetail.value ||
                canEditPage.value ||
                canChangePageStatus.value
            )
        })

        /* 根据当前页面生成可见的操作选项 */
        const getPageActionItems = (page) => {
            return [
                {
                    key: 'detail',
                    label: '查看详情',
                    icon: 'bi bi-eye',
                    visible: canViewPageDetail.value,
                },
                {
                    key: 'edit',
                    label: '编辑页面',
                    icon: 'bi bi-pencil',
                    visible: canEditPage.value,
                },
                {
                    key: 'status',
                    label: page.is_active
                        ? '停用页面'
                        : '启用页面',
                    icon: page.is_active
                        ? 'bi bi-slash-circle'
                        : 'bi bi-check-circle',
                    danger: page.is_active,
                    visible: canChangePageStatus.value,
                },
            ]
        }

        /* 执行页面菜单操作 */
        const handlePageAction = (action, page) => {
            if (!page) {
                return
            }

            switch (action) {
                case 'detail':
                    openDetailModal(page)
                    break
                case 'edit':
                    openEditModal(page)
                    break
                case 'status':
                    openStatusModal(page)
                    break
                default:
                    break
            }
        }

        /* ==================== 页面与角色数据 ==================== */

        const pages = ref([])
        const roles = ref([])

        const loading = ref(false)
        const errorMessage = ref('')

        /* ==================== 加载页面列表 ==================== */

        const loadPages = async () => {
            if (!canViewPageList.value) {
                pages.value = []
                errorMessage.value =
                    '当前用户没有查看页面列表的权限'

                return
            }

            pages.value = await getPagesApi()
        }

        /* ==================== 加载角色列表 ==================== */

        const loadRoles = async () => {
            /*
             * 只有配置页面角色时才需要角色选项。
             *
             * 角色列表接口还需要 ROLE_LIST 权限。
             */
            if (
                !canAssignPageRole.value ||
                !authStore.hasPermission('ROLE_LIST')
            ) {
                roles.value = []
                return
            }

            roles.value = await getRolesApi()
        }

        /* ==================== 初始化管理数据 ==================== */

        const loadPageData = async () => {
            errorMessage.value = ''
            loading.value = true

            try {
                await Promise.all([
                    loadPages(),
                    loadRoles(),
                ])
            } catch (error) {
                errorMessage.value =
                    error.userMessage ||
                    error.message ||
                    '页面管理数据加载失败'
            } finally {
                loading.value = false
            }
        }

        onMounted(loadPageData)

        /* ==================== 刷新导航数据 ==================== */

        /*
         * 页面发生创建、编辑或状态变化后，
         * 同步刷新顶部导航和侧边栏。
         */
        const refreshNavigation = async () => {
            try {
                navigationStore.clearPages()
                await navigationStore.loadPages()
            } catch (error) {
                /*
                 * 页面数据已经修改成功时，
                 * 导航刷新失败不应把整个操作判断为失败。
                 */
                message.warning(
                    '页面已保存，但导航刷新失败，请刷新浏览器',
                )
            }
        }

        /* ==================== 搜索与筛选 ==================== */

        const keyword = ref('')
        const statusFilter = ref('all')

        const filteredPages = computed(() => {
            const search =
                keyword.value.trim().toLowerCase()

            return pages.value.filter((page) => {
                /*
                 * 搜索范围：
                 * 页面名称、编码、路由、组件和父页面名称。
                 */
                const searchContent = [
                    page.name,
                    page.code,
                    page.path,
                    page.component,
                    page.parent?.name,
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
                        page.is_active
                    ) ||
                    (
                        statusFilter.value === 'disabled' &&
                        !page.is_active
                    )

                return (
                    matchesKeyword &&
                    matchesStatus
                )
            })
        })

        /* ==================== 页面统计 ==================== */

        const activeCount = computed(() => {
            return pages.value.filter((page) => {
                return page.is_active
            }).length
        })

        const disabledCount = computed(() => {
            return pages.value.length -
                activeCount.value
        })

        const rootPageCount = computed(() => {
            return pages.value.filter((page) => {
                return !page.parent
            }).length
        })

        /* ==================== 显示模式 ==================== */

        const viewMode = ref('list')

        const setViewMode = (mode) => {
            if (!['list', 'card'].includes(mode)) {
                return
            }

            viewMode.value = mode
        }

        /* ==================== 页面展示辅助 ==================== */

        const getPageIcon = (page) => {
            return (
                page?.icon ||
                DEFAULT_PAGE_ICON
            )
        }

        const getParentName = (page) => {
            return page?.parent?.name ||
                '顶级页面'
        }

        const getVisibleRoleNames = (page) => {
            const roleList =
                page?.visible_roles || []

            if (roleList.length === 0) {
                return '未分配角色'
            }

            return roleList
                .map((role) => role.name)
                .join('、')
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

        /* ==================== 下拉选项 ==================== */

        /*
         * 可见角色只能选择当前启用的角色，
         * 与后端 visible_role_ids 的限制保持一致。
         */
        const roleOptions = computed(() => {
            return roles.value
                .filter((role) => role.is_active)
                .map((role) => {
                    return {
                        label:
                            `${role.name} · ${role.code}`,
                        value: role.id,
                    }
                })
        })

        /*
         * 找出指定页面的全部子孙页面 ID，
         * 编辑时不能将这些页面设置成自己的父页面。
         */
        const getDescendantIds = (pageId) => {
            const descendantIds = new Set()
            const pendingIds = [pageId]

            while (pendingIds.length > 0) {
                const currentId =
                    pendingIds.shift()

                pages.value.forEach((page) => {
                    if (
                        page.parent?.id === currentId &&
                        !descendantIds.has(page.id)
                    ) {
                        descendantIds.add(page.id)
                        pendingIds.push(page.id)
                    }
                })
            }

            return descendantIds
        }

        /*
         * 父页面选择项。
         *
         * 创建时可以选择任意已启用页面。
         * 编辑时排除当前页面和它的全部子孙页面，
         * 防止形成循环层级。
         */
        const parentPageOptions = computed(() => {
            const excludedIds = new Set()

            if (editingPage.value) {
                excludedIds.add(
                    editingPage.value.id,
                )

                getDescendantIds(
                    editingPage.value.id,
                ).forEach((id) => {
                    excludedIds.add(id)
                })
            }

            const options = pages.value
                .filter((page) => {
                    return !excludedIds.has(page.id)
                })
                .map((page) => {
                    return {
                        label:
                            `${page.name} · ${page.path}`,
                        value: page.id,
                        icon: getPageIcon(page),
                        disabled: !page.is_active,
                    }
                })

            return [
                {
                    label: '顶级页面',
                    value: null,
                    icon: 'bi bi-diagram-3',
                },
                ...options,
            ]
        })

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

        const submitting = ref(false)

        /* ==================== 页面表单状态 ==================== */

        const formMode = ref('create')
        const formModalVisible = ref(false)
        const editingPage = ref(null)

        const pageForm = reactive(
            createInitialForm(),
        )

        const isCreateMode = computed(() => {
            return formMode.value === 'create'
        })

        const formModalTitle = computed(() => {
            return isCreateMode.value
                ? '创建页面'
                : '编辑页面'
        })

        /* ==================== 重置页面表单 ==================== */

        const resetPageForm = () => {
            Object.assign(
                pageForm,
                createInitialForm(),
            )

            editingPage.value = null
        }

        /* ==================== 打开创建弹出层 ==================== */

        const openCreateModal = () => {
            if (!canCreatePage.value) {
                message.warning(
                    '当前用户没有创建页面的权限',
                )

                return
            }

            resetPageForm()

            formMode.value = 'create'
            formModalVisible.value = true
        }

        /* ==================== 打开编辑弹出层 ==================== */

        const openEditModal = (page) => {
            if (!canEditPage.value) {
                message.warning(
                    '当前用户没有修改页面的权限',
                )

                return
            }

            if (!page) {
                return
            }

            resetPageForm()

            editingPage.value = page
            formMode.value = 'edit'

            pageForm.name = page.name || ''
            pageForm.code = page.code || ''
            pageForm.path = page.path || ''
            pageForm.component =
                page.component || ''
            pageForm.icon =
                page.icon || DEFAULT_PAGE_ICON
            pageForm.parentId =
                page.parent?.id ?? null
            pageForm.visibleRoleIds =
                (page.visible_roles || [])
                    .map((role) => role.id)
            pageForm.sortOrder =
                Number(page.sort_order) || 0
            pageForm.isActive =
                Boolean(page.is_active)

            formModalVisible.value = true
        }

        /* ==================== 关闭页面表单 ==================== */

        const closeFormModal = () => {
            if (submitting.value) {
                return
            }

            formModalVisible.value = false
        }

        /* ==================== 规范化页面编码 ==================== */

        const normalizePageCode = () => {
            pageForm.code =
                pageForm.code
                    .trim()
                    .toUpperCase()
        }

        /* ==================== 页面表单验证 ==================== */

        const validatePageForm = () => {
            const name =
                pageForm.name.trim()

            const code =
                pageForm.code.trim().toUpperCase()

            const path =
                pageForm.path.trim()

            const component =
                pageForm.component.trim()

            const icon =
                pageForm.icon.trim()

            const sortOrder =
                Number(pageForm.sortOrder)

            if (!name) {
                message.warning('请输入页面名称')
                return false
            }

            if (name.length > 100) {
                message.warning(
                    '页面名称不能超过100个字符',
                )

                return false
            }

            if (!code) {
                message.warning('请输入页面编码')
                return false
            }

            if (
                !/^[A-Za-z][A-Za-z0-9_]*$/.test(
                    code,
                )
            ) {
                message.warning(
                    '页面编码必须以字母开头，且只能包含字母、数字和下划线',
                )

                return false
            }

            if (code.length > 100) {
                message.warning(
                    '页面编码不能超过100个字符',
                )

                return false
            }

            if (!path) {
                message.warning('请输入页面路由')
                return false
            }

            if (!path.startsWith('/')) {
                message.warning(
                    '页面路由必须以 / 开头',
                )

                return false
            }

            if (/\s/.test(path)) {
                message.warning(
                    '页面路由不能包含空格',
                )

                return false
            }

            if (path.length > 255) {
                message.warning(
                    '页面路由不能超过255个字符',
                )

                return false
            }

            if (component.length > 255) {
                message.warning(
                    '前端组件路径不能超过255个字符',
                )

                return false
            }

            if (icon.length > 100) {
                message.warning(
                    '页面图标不能超过100个字符',
                )

                return false
            }

            if (
                !Number.isInteger(sortOrder) ||
                sortOrder < 0
            ) {
                message.warning(
                    '页面排序必须是大于或等于0的整数',
                )

                return false
            }

            pageForm.name = name
            pageForm.code = code
            pageForm.path = path
            pageForm.component = component
            pageForm.icon =
                icon || DEFAULT_PAGE_ICON
            pageForm.sortOrder = sortOrder

            return true
        }

        /* ==================== 生成页面资料数据 ==================== */

        /*
         * 页面资料接口只接收页面自身字段。
         *
         * 以下内容不能混入：
         * visible_role_ids
         * is_active
         */
        const createPageData = () => {
            return {
                name: pageForm.name,
                code: pageForm.code,
                path: pageForm.path,
                component:
                    pageForm.component,
                icon: pageForm.icon,
                parent_id:
                    pageForm.parentId,
                sort_order:
                    pageForm.sortOrder,
            }
        }

        /* ==================== 创建页面 ==================== */

        const createPage = async () => {
            /*
             * 第一步：创建页面基础资料。
             */
            const createdPage =
                await createPageApi(
                    createPageData(),
                )

            const followUpErrors = []

            /*
             * 第二步：配置页面可见角色。
             *
             * 只有同时拥有 PAGE_ASSIGN_ROLE 时执行。
             */
            if (
                canAssignPageRole.value &&
                pageForm.visibleRoleIds.length > 0
            ) {
                try {
                    await updatePageRolesApi(
                        createdPage.id,
                        pageForm.visibleRoleIds,
                    )
                } catch (error) {
                    followUpErrors.push(
                        getErrorMessage(
                            error,
                            '可见角色配置失败',
                        ),
                    )
                }
            }

            /*
             * 第三步：设置页面初始状态。
             *
             * 页面创建后默认启用。
             * 选择停用时调用独立状态接口。
             */
            if (
                canChangePageStatus.value &&
                !pageForm.isActive
            ) {
                try {
                    await updatePageStatusApi(
                        createdPage.id,
                        false,
                    )
                } catch (error) {
                    followUpErrors.push(
                        getErrorMessage(
                            error,
                            '页面状态设置失败',
                        ),
                    )
                }
            }

            await loadPages()
            await refreshNavigation()

            if (followUpErrors.length) {
                message.warning(
                    `页面已创建，但${followUpErrors.join('；')}`,
                )

                return
            }

            formModalVisible.value = false

            message.success('页面创建成功')
        }

        /* ==================== 编辑页面 ==================== */

        const updatePage = async () => {
            if (!editingPage.value) {
                return
            }

            const pageId =
                editingPage.value.id

            const followUpErrors = []

            /*
             * 拥有 PAGE_UPDATE 时，
             * 才修改页面基础资料。
             */
            if (canUpdatePage.value) {
                try {
                    await updatePageApi(
                        pageId,
                        createPageData(),
                    )
                } catch (error) {
                    followUpErrors.push(
                        getErrorMessage(
                            error,
                            '页面资料修改失败',
                        ),
                    )
                }
            }

            /*
             * 拥有 PAGE_ASSIGN_ROLE 时，
             * 使用独立接口替换页面全部可见角色。
             *
             * 空数组表示清空可见角色。
             */
            if (canAssignPageRole.value) {
                try {
                    await updatePageRolesApi(
                        pageId,
                        pageForm.visibleRoleIds,
                    )
                } catch (error) {
                    followUpErrors.push(
                        getErrorMessage(
                            error,
                            '页面可见角色配置失败',
                        ),
                    )
                }
            }

            await loadPages()
            await refreshNavigation()

            if (followUpErrors.length) {
                message.warning(
                    followUpErrors.join('；'),
                )

                return
            }

            formModalVisible.value = false

            message.success('页面信息修改成功')
        }

        /* ==================== 提交页面表单 ==================== */

        const submitPageForm = async () => {
            if (
                submitting.value ||
                !validatePageForm()
            ) {
                return
            }

            submitting.value = true

            try {
                if (isCreateMode.value) {
                    await createPage()
                } else {
                    await updatePage()
                }
            } catch (error) {
                message.error(
                    getErrorMessage(
                        error,
                        isCreateMode.value
                            ? '页面创建失败'
                            : '页面修改失败',
                    ),
                )
            } finally {
                submitting.value = false
            }
        }

        /* ==================== 页面详情弹出层 ==================== */

        const detailModalVisible = ref(false)
        const detailLoading = ref(false)
        const selectedPage = ref(null)

        const openDetailModal = async (page) => {
            if (!canViewPageDetail.value) {
                message.warning(
                    '当前用户没有查看页面详情的权限',
                )

                return
            }

            if (!page || detailLoading.value) {
                return
            }

            detailModalVisible.value = true
            detailLoading.value = true
            selectedPage.value = null

            try {
                selectedPage.value =
                    await getPageDetailApi(page.id)
            } catch (error) {
                detailModalVisible.value = false

                message.error(
                    getErrorMessage(
                        error,
                        '页面信息加载失败',
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

        const editSelectedPage = () => {
            if (!selectedPage.value) {
                return
            }

            detailModalVisible.value = false
            openEditModal(selectedPage.value)
        }

        /* ==================== 状态确认弹出层 ==================== */

        const statusModalVisible = ref(false)
        const statusTargetPage = ref(null)

        const openStatusModal = (page) => {
            if (!canChangePageStatus.value) {
                message.warning(
                    '当前用户没有修改页面状态的权限',
                )

                return
            }

            if (!page) {
                return
            }

            statusTargetPage.value = page
            statusModalVisible.value = true
        }

        const closeStatusModal = () => {
            if (submitting.value) {
                return
            }

            statusModalVisible.value = false
        }

        const statusModalTitle = computed(() => {
            return statusTargetPage.value
                ?.is_active
                ? '停用页面'
                : '启用页面'
        })

        const statusActionText = computed(() => {
            return statusTargetPage.value
                ?.is_active
                ? '确认停用'
                : '确认启用'
        })

        const confirmPageStatus = async () => {
            if (
                submitting.value ||
                !statusTargetPage.value
            ) {
                return
            }

            submitting.value = true

            const target =
                statusTargetPage.value

            const shouldEnable =
                !target.is_active

            try {
                /*
                * 新版后端统一使用页面状态接口。
                */
                await updatePageStatusApi(
                    target.id,
                    shouldEnable,
                )

                await loadPages()
                await refreshNavigation()

                statusModalVisible.value = false

                message.success(
                    shouldEnable
                        ? '页面已启用'
                        : '页面已停用',
                )
            } catch (error) {
                message.error(
                    getErrorMessage(
                        error,
                        shouldEnable
                            ? '页面启用失败'
                            : '页面停用失败',
                    ),
                )
            } finally {
                submitting.value = false
            }
        }

        /* ==================== 向模板暴露内容 ==================== */

        return {
            /* ==================== 操作权限 ==================== */

            canViewPageList,
            canViewPageDetail,
            canCreatePage,
            canUpdatePage,
            canChangePageStatus,
            canAssignPageRole,
            canEditPage,

            /* ==================== 页面操作菜单 ==================== */

            hasPageActions,
            getPageActionItems,
            handlePageAction,

            pages,
            roles,
            loading,
            errorMessage,
            loadPageData,

            keyword,
            statusFilter,
            statusFilterOptions,
            filteredPages,

            activeCount,
            disabledCount,
            rootPageCount,

            viewMode,
            setViewMode,

            getPageIcon,
            getParentName,
            getVisibleRoleNames,
            formatTime,

            bootstrapIconOptions,
            parentPageOptions,
            roleOptions,
            pageStatusOptions,

            submitting,

            formMode,
            formModalVisible,
            formModalTitle,
            isCreateMode,
            pageForm,
            openCreateModal,
            openEditModal,
            closeFormModal,
            normalizePageCode,
            submitPageForm,

            detailModalVisible,
            detailLoading,
            selectedPage,
            openDetailModal,
            closeDetailModal,
            editSelectedPage,

            statusModalVisible,
            statusTargetPage,
            statusModalTitle,
            statusActionText,
            openStatusModal,
            closeStatusModal,
            confirmPageStatus,
        }
    },
})
