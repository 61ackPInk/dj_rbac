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

/* ==================== 页面与角色接口 ==================== */

import {
    createPageApi,
    disablePageApi,
    enablePageApi,
    getPageDetailApi,
    getPagesApi,
    updatePageApi,
} from '@/api/pages'

import { getRolesApi } from '@/api/roles'

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
    },

    setup() {
        const authStore = useAuthStore()
        const navigationStore =
            useNavigationStore()

        /* ==================== 当前用户权限 ==================== */

        /*
         * 页面管理接口只允许根管理员访问。
         */
        const canManagePages = computed(() => {
            return Boolean(authStore.user?.is_root)
        })

        /* ==================== 页面与角色数据 ==================== */

        const pages = ref([])
        const roles = ref([])

        const loading = ref(false)
        const errorMessage = ref('')

        /* ==================== 加载页面列表 ==================== */

        const loadPages = async () => {
            if (!canManagePages.value) {
                pages.value = []

                throw new Error(
                    '当前用户无权查看页面列表',
                )
            }

            pages.value = await getPagesApi()
        }

        /* ==================== 加载角色列表 ==================== */

        const loadRoles = async () => {
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
            if (!canManagePages.value) {
                message.warning(
                    '当前用户无权创建页面',
                )

                return
            }

            resetPageForm()

            formMode.value = 'create'
            formModalVisible.value = true
        }

        /* ==================== 打开编辑弹出层 ==================== */

        const openEditModal = (page) => {
            if (!canManagePages.value) {
                message.warning(
                    '当前用户无权编辑页面',
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

        /* ==================== 生成提交数据 ==================== */

        const createSubmitData = () => {
            return {
                name: pageForm.name,
                code: pageForm.code,
                path: pageForm.path,
                component:
                    pageForm.component,
                icon: pageForm.icon,
                parent_id:
                    pageForm.parentId,
                visible_role_ids:
                    pageForm.visibleRoleIds,
                sort_order:
                    pageForm.sortOrder,
                is_active:
                    pageForm.isActive,
            }
        }

        /* ==================== 创建页面 ==================== */

        const createPage = async () => {
            await createPageApi(
                createSubmitData(),
            )

            await loadPages()
            await refreshNavigation()

            formModalVisible.value = false

            message.success('页面创建成功')
        }

        /* ==================== 编辑页面 ==================== */

        const updatePage = async () => {
            if (!editingPage.value) {
                return
            }

            await updatePageApi(
                editingPage.value.id,
                createSubmitData(),
            )

            await loadPages()
            await refreshNavigation()

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
            if (!canManagePages.value) {
                message.warning(
                    '当前用户无权修改页面状态',
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
                if (shouldEnable) {
                    await enablePageApi(target.id)
                } else {
                    await disablePageApi(target.id)
                }

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
            canManagePages,

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