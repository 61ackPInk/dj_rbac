/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
  onMounted,
  ref,
} from 'vue'

/* ==================== 公共组件 ==================== */

import AppSelect from '@/components/form/select/app-select.vue'
import AppCopyText from '@/components/common/copy-text/copy-text.vue'

/* ==================== 商品组合接口与权限 ==================== */

import {
  getProductBundlesApi,
  getProductWarehousesApi,
} from '@/api/product-bundles'
import { useAuthStore } from '@/stores/auth'

/* ==================== 商品组合页面 ==================== */

export default {
  name: 'ProductBundlesView',

  components: {
    AppSelect,
    AppCopyText,
  },

  setup() {
    const authStore = useAuthStore()

    /* ==================== 操作权限 ==================== */

    /*
     * 页面访问由路由中的 PRODUCT_BUNDLE 控制。
     * 仓库及组合列表接口由 PRODUCT_BUNDLE_LIST 控制。
     */
    const canViewBundleList = computed(() => {
      return authStore.hasPermission(
        'PRODUCT_BUNDLE_LIST',
      )
    })

    /* ==================== 仓库状态 ==================== */

    const warehouses = ref([])
    const warehouseCode = ref(undefined)
    const warehouseLoading = ref(false)
    const warehouseError = ref('')

    /*
     * AppSelect 使用仓库编码作为 value，
     * 使用仓库名称作为展示文本。
     */
    const warehouseOptions = computed(() => {
      return warehouses.value.map((warehouse) => {
        return {
          label: `${warehouse.name}-${warehouse.code}`,
          value: warehouse.code,
        }
      })
    })

    const warehousePlaceholder = computed(() => {
      if (warehouseLoading.value) {
        return '正在加载仓库'
      }

      if (warehouses.value.length === 0) {
        return '暂无可用仓库'
      }

      return '请选择仓库'
    })

    /* ==================== 显示模式 ==================== */

    /*
     * 切换显示模式只改变当前页的前端展示，
     * 不会重新请求组合列表。
     */
    const viewMode = ref('list')

    const setViewMode = (mode) => {
      if (!['list', 'card'].includes(mode)) {
        return
      }

      viewMode.value = mode
    }

    /* ==================== 组合列表状态 ==================== */

    const bundles = ref([])
    const bundleLoading = ref(false)
    const bundleError = ref('')

    /* ==================== 当前页即时搜索 ==================== */

    /*
     * 搜索只过滤当前接口已经返回的数据，
     * 输入内容时不会重新请求后端。
     */
    const keyword = ref('')

    const displayedBundles = computed(() => {
      const search =
        keyword.value.trim().toLowerCase()

      if (!search) {
        return bundles.value
      }

      return bundles.value.filter((bundle) => {
        const components =
          Array.isArray(bundle?.components)
            ? bundle.components
            : []

        const componentContent = components
          .map((component) => {
            return [
              component?.customer_sku,
              component?.name,
            ]
              .filter(Boolean)
              .join(' ')
          })
          .join(' ')

        const searchableContent = [
          bundle?.name,
          bundle?.bundle_sku,
          componentContent,
        ]
          .filter(Boolean)
          .join(' ')
          .toLowerCase()

        return searchableContent.includes(search)
      })
    })

    const clearSearch = () => {
      keyword.value = ''
    }

    /* ==================== 组合分页状态 ==================== */

    const page = ref(1)
    const pageSize = ref(20)
    const total = ref(0)

    const pageSizeOptions = [
      {
        label: '每页 20 条',
        value: 20,
      },
      {
        label: '每页 50 条',
        value: 50,
      },
      {
        label: '每页 100 条',
        value: 100,
      },
    ]

    const totalPages = computed(() => {
      return Math.max(
        1,
        Math.ceil(
          total.value / pageSize.value,
        ),
      )
    })

    const canGoPrevious = computed(() => {
      return page.value > 1
    })

    const canGoNext = computed(() => {
      return page.value < totalPages.value
    })

    /* ==================== 数据格式化 ==================== */

    const formatQuantity = (value) => {
      if (value === null || value === undefined) {
        return '-'
      }

      return value
    }

    const formatDateTime = (value) => {
      if (!value) {
        return '-'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        return value
      }

      return date.toLocaleString('zh-CN', {
        hour12: false,
      })
    }

    /* ==================== 加载组合列表 ==================== */

    const loadBundles = async () => {
      /*
       * 没有操作权限或尚未选择仓库时，
       * 不发送组合列表请求。
       */
      if (
        !canViewBundleList.value ||
        !warehouseCode.value
      ) {
        bundles.value = []
        total.value = 0
        bundleError.value = ''

        return false
      }

      if (bundleLoading.value) {
        return false
      }

      bundleLoading.value = true
      bundleError.value = ''

      try {
        const result =
          await getProductBundlesApi({
            warehouse_code:
              warehouseCode.value,
            page: page.value,
            page_size: pageSize.value,
          })

        bundles.value =
          Array.isArray(result?.items)
            ? result.items
            : []

        const pagination =
          result?.pagination || {}

        page.value =
          Number(pagination.page) ||
          page.value

        pageSize.value =
          Number(pagination.page_size) ||
          pageSize.value

        total.value =
          Number(pagination.total) || 0

        return true
      } catch (error) {
        bundles.value = []
        total.value = 0

        if (
          error.status === 502 ||
          error.status === 503
        ) {
          bundleError.value =
            '第三方 ERP 数据暂时不可用，请稍后重试'
        } else if (error.status === 403) {
          bundleError.value =
            '当前用户没有 PRODUCT_BUNDLE_LIST 权限'
        } else {
          bundleError.value =
            error.userMessage ||
            '商品组合列表加载失败'
        }

        return false
      } finally {
        bundleLoading.value = false
      }
    }

    /* ==================== 加载仓库 ==================== */

    const loadWarehouses = async () => {
      /*
       * 页面可见不代表拥有列表操作权限。
       * 没有操作权限时不发送仓库接口请求。
       */
      if (!canViewBundleList.value) {
        warehouses.value = []
        warehouseCode.value = undefined
        warehouseError.value = ''

        return
      }

      if (warehouseLoading.value) {
        return
      }

      warehouseLoading.value = true
      warehouseError.value = ''

      try {
        const result =
          await getProductWarehousesApi()

        warehouses.value =
          Array.isArray(result?.items)
            ? result.items
            : []

        /*
         * 当前只有一个仓库时自动选中。
         * 不在前端写死任何仓库编码。
         */
        if (warehouses.value.length === 1) {
          warehouseCode.value =
            warehouses.value[0].code

          page.value = 1
          await loadBundles()
        } else {
          warehouseCode.value = undefined
          bundles.value = []
          total.value = 0
        }
      } catch (error) {
        warehouses.value = []
        warehouseCode.value = undefined

        if (
          error.status === 502 ||
          error.status === 503
        ) {
          warehouseError.value =
            '第三方 ERP 数据暂时不可用，请稍后重试'
        } else if (error.status === 403) {
          warehouseError.value =
            '当前用户没有 PRODUCT_BUNDLE_LIST 权限'
        } else {
          warehouseError.value =
            error.userMessage ||
            '仓库列表加载失败'
        }
      } finally {
        warehouseLoading.value = false
      }
    }

    /* ==================== 切换仓库 ==================== */

    const handleWarehouseChange = () => {
      page.value = 1
      bundles.value = []
      total.value = 0

      loadBundles()
    }

    /* ==================== 分页操作 ==================== */

    const changePageSize = () => {
      page.value = 1
      loadBundles()
    }

    const goToPreviousPage = () => {
      if (
        bundleLoading.value ||
        !canGoPrevious.value
      ) {
        return
      }

      page.value -= 1
      loadBundles()
    }

    const goToNextPage = () => {
      if (
        bundleLoading.value ||
        !canGoNext.value
      ) {
        return
      }

      page.value += 1
      loadBundles()
    }

    onMounted(loadWarehouses)

    return {
      canViewBundleList,

      warehouses,
      warehouseCode,
      warehouseOptions,
      warehousePlaceholder,
      warehouseLoading,
      warehouseError,

      viewMode,
      setViewMode,

      bundles,
      keyword,
      displayedBundles,
      bundleLoading,
      bundleError,

      page,
      pageSize,
      total,
      pageSizeOptions,
      totalPages,
      canGoPrevious,
      canGoNext,

      loadWarehouses,
      handleWarehouseChange,
      loadBundles,
      changePageSize,
      goToPreviousPage,
      goToNextPage,

      formatQuantity,
      formatDateTime,
      clearSearch,
    }
  },
}
