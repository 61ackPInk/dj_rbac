/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
  onMounted,
  ref,
} from 'vue'

/* ==================== 公共组件 ==================== */

import AppSelect from '@/components/form/select/app-select.vue'

/* ==================== 商品接口与权限 ==================== */

import { getProductsApi } from '@/api/products'
import { useAuthStore } from '@/stores/auth'

/* ==================== 商品列表页面 ==================== */

export default {
  name: 'ProductListView',

  components: {
    AppSelect,
  },

  setup() {
    const authStore = useAuthStore()

    /* ==================== 操作权限 ==================== */

    /*
     * 页面访问由路由中的 PRODUCT_LIST 页面编码控制。
     * 商品列表接口还需要 PRODUCT_LIST 操作权限。
     */
    const canViewProductList = computed(() => {
      return authStore.hasPermission(
        'PRODUCT_LIST',
      )
    })

    /* ==================== 商品列表状态 ==================== */

    const products = ref([])
    const loading = ref(false)
    const errorMessage = ref('')

    /* ==================== 显示模式 ==================== */

    /*
     * list：列表模式。
     * card：卡片模式。
     *
     * 切换模式只改变前端展示，不重新请求 ERP 数据。
     */
    const viewMode = ref('list')

    const setViewMode = (mode) => {
      if (!['list', 'card'].includes(mode)) {
        return
      }

      viewMode.value = mode
    }

    /* ==================== 分页状态 ==================== */

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

    const resultStart = computed(() => {
      if (total.value === 0) {
        return 0
      }

      return (
        (page.value - 1) *
          pageSize.value +
        1
      )
    })

    const resultEnd = computed(() => {
      return Math.min(
        page.value * pageSize.value,
        total.value,
      )
    })

    const canGoPrevious = computed(() => {
      return page.value > 1
    })

    const canGoNext = computed(() => {
      return page.value < totalPages.value
    })

    /* ==================== 加载商品列表 ==================== */

    const loadProducts = async () => {
      /*
       * 页面可见不代表拥有列表操作权限。
       * 没有操作权限时不发送商品接口请求。
       */
      if (!canViewProductList.value) {
        products.value = []
        total.value = 0
        errorMessage.value = ''

        return
      }

      if (loading.value) {
        return
      }

      loading.value = true
      errorMessage.value = ''

      try {
        const result =
          await getProductsApi({
            page: page.value,
            page_size: pageSize.value,
          })

        products.value =
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
      } catch (error) {
        products.value = []
        total.value = 0

        errorMessage.value =
          error.userMessage ||
          '商品列表加载失败'
      } finally {
        loading.value = false
      }
    }

    onMounted(loadProducts)

    /* ==================== 分页操作 ==================== */

    const changePageSize = () => {
      page.value = 1
      loadProducts()
    }

    const goToPreviousPage = () => {
      if (
        loading.value ||
        !canGoPrevious.value
      ) {
        return
      }

      page.value -= 1
      loadProducts()
    }

    const goToNextPage = () => {
      if (
        loading.value ||
        !canGoNext.value
      ) {
        return
      }

      page.value += 1
      loadProducts()
    }

    /* ==================== 商品图片 ==================== */

    /*
     * 记录当前页面加载失败的商品图片。
     *
     * 不直接修改接口返回的 product.images，
     * 避免污染后端原始数据。
     */
    const failedImageKeys = ref(
      new Set(),
    )

    const getProductKey = (product) => {
      return String(
        product?.id ||
        product?.customer_sku ||
        '',
      )
    }

    /*
     * 商品列表和卡片均使用 images 中的第一张有效图片。
     * 完整图片列表留到商品详情弹窗展示。
     */
    const getProductImage = (product) => {
      if (!Array.isArray(product?.images)) {
        return ''
      }

      return (
        product.images.find((image) => {
          return (
            typeof image === 'string' &&
            image.trim()
          )
        }) || ''
      )
    }

    const hasProductImage = (product) => {
      const imageUrl =
        getProductImage(product)

      if (!imageUrl) {
        return false
      }

      return !failedImageKeys.value.has(
        getProductKey(product),
      )
    }

    const handleProductImageError = (
      product,
    ) => {
      const nextFailedKeys = new Set(
        failedImageKeys.value,
      )

      nextFailedKeys.add(
        getProductKey(product),
      )

      /*
       * 使用新 Set 替换原值，
       * 保证 Vue 能检测到状态变化。
       */
      failedImageKeys.value =
        nextFailedKeys
    }

    /* ==================== 商品展示辅助方法 ==================== */

    /*
     * null 表示数量未知，显示“—”；
     * 0 是真实数量，必须显示为 0。
     */
    const formatQuantity = (value) => {
      return value == null
        ? '—'
        : value
    }

    const getProductName = (product) => {
      return (
        product?.name ||
        product?.english_name ||
        '未命名商品'
      )
    }

    const getWarehouseName = (product) => {
      const warehouse =
        product?.main_warehouse

      if (!warehouse) {
        return '—'
      }

      if (
        warehouse.name &&
        warehouse.code
      ) {
        return (
          `${warehouse.name} ` +
          `(${warehouse.code})`
        )
      }

      return (
        warehouse.name ||
        warehouse.code ||
        '—'
      )
    }

    const getInventoryStateText = (
      product,
    ) => {
      if (
        product?.inventory?.found === false
      ) {
        return '未匹配库存'
      }

      return (
        product?.inventory
          ?.status_name ||
        '—'
      )
    }

    /* ==================== 向模板暴露内容 ==================== */

    return {
      canViewProductList,

      products,
      loading,
      errorMessage,
      loadProducts,

      viewMode,
      setViewMode,

      page,
      pageSize,
      total,
      totalPages,
      resultStart,
      resultEnd,
      pageSizeOptions,
      canGoPrevious,
      canGoNext,
      changePageSize,
      goToPreviousPage,
      goToNextPage,

      getProductImage,
      hasProductImage,
      handleProductImageError,

      formatQuantity,
      getProductName,
      getWarehouseName,
      getInventoryStateText,
    }
  },
}