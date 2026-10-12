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
     * 页面可见性由路由中的 PRODUCT_LIST 页面编码控制。
     * 进入页面后，列表接口还要单独检查 PRODUCT_LIST 操作权限。
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
       * 页面可见不代表拥有查看列表操作权限。
       * 没有权限时不发送接口请求。
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

        /*
         * 分页信息以后端返回值为准。
         * Number 转换避免后端数字字符串影响分页计算。
         */
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

    /* ==================== 商品展示辅助方法 ==================== */

    /*
     * 必须使用 value == null 判断。
     *
     * null 表示未知，显示“—”；
     * 0 表示真实的零库存，必须显示为 0。
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

      formatQuantity,
      getProductName,
      getWarehouseName,
      getInventoryStateText,
    }
  },
}