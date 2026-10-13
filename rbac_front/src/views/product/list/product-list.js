/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
  onMounted,
  ref,
} from 'vue'

/* ==================== 公共组件 ==================== */

import AppSelect from '@/components/form/select/app-select.vue'
import AppCopyText from '@/components/common/copy-text/copy-text.vue'
import AppModal from '@/components/feedback/modal/app-modal.vue'

/* ==================== 商品接口与权限 ==================== */

import {
  getProductDetailApi,
  getProductsApi,
} from '@/api/products'
import { useAuthStore } from '@/stores/auth'
import { message } from '@/utils/message'

/* ==================== 商品列表页面 ==================== */

export default {
  name: 'ProductListView',

  components: {
    AppSelect,
    AppModal,
    AppCopyText,
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

    /* ==================== 商品详情权限 ==================== */

    const canViewProductDetail = computed(() => {
      return authStore.hasPermission(
        'PRODUCT_DETAIL',
      )
    })

    /* ==================== 商品列表状态 ==================== */

    const products = ref([])
    const loading = ref(false)
    const errorMessage = ref('')

    /* ==================== 当前页搜索与筛选 ==================== */

    /*
     * 搜索、库存状态筛选和排序只作用于
     * 当前接口已经返回的这一页商品。
     *
     * 切换条件不会重新请求后端。
     */
    const keyword = ref('')
    const inventoryFilter = ref('all')
    const sortMode = ref('default')

    const sortOptions = [
      {
        label: '默认排序',
        value: 'default',
      },
      {
        label: '商品名称 A-Z',
        value: 'name_asc',
      },
      {
        label: '总库存 高-低',
        value: 'total_desc',
      },
      {
        label: '总库存 低-高',
        value: 'total_asc',
      },
      {
        label: '更新时间 最新',
        value: 'updated_desc',
      },
    ]

    /* ==================== 库存状态判断 ==================== */

    const getInventoryCategory = (
      product,
    ) => {
      const inventory =
        product?.inventory

      /*
       * 没有匹配到库存记录，或者可用库存未知，
       * 都不能当成真实的零库存。
       */
      if (
        inventory?.found === false ||
        inventory?.available == null
      ) {
        return 'unknown'
      }

      const available =
        Number(inventory.available)

      if (Number.isNaN(available)) {
        return 'unknown'
      }

      if (available === 0) {
        return 'out_of_stock'
      }

      if (
        available > 0 &&
        available < 50
      ) {
        return 'low_stock'
      }

      if (available >= 50) {
        return 'in_stock'
      }

      return 'unknown'
    }

    /* ==================== 当前页库存统计 ==================== */

    const currentPageInventoryCounts = computed(() => {
      const counts = {
        all: products.value.length,
        in_stock: 0,
        low_stock: 0,
        out_of_stock: 0,
        unknown: 0,
      }

      products.value.forEach((product) => {
        const category =
          getInventoryCategory(product)

        counts[category] += 1
      })

      return counts
    })

    /* ==================== 当前页商品处理 ==================== */

    const displayedProducts = computed(() => {
      const search =
        keyword.value.trim().toLowerCase()

      /*
       * 先筛选，再复制数组进行排序。
       * 不直接修改接口返回的 products 原数组。
       */
      const result = products.value.filter(
        (product) => {
          const searchContent = [
            product?.name,
            product?.english_name,
            product?.customer_sku,
            product?.erp_sku,
            product?.reference_code,
          ]
            .filter((value) => {
              return value != null
            })
            .join(' ')
            .toLowerCase()

          const matchesKeyword =
            !search ||
            searchContent.includes(search)

          const matchesInventory =
            inventoryFilter.value === 'all' ||
            getInventoryCategory(product) ===
            inventoryFilter.value

          return (
            matchesKeyword &&
            matchesInventory
          )
        },
      )

      if (sortMode.value === 'default') {
        return result
      }

      return [...result].sort(
        (productA, productB) => {
          /* 商品名称 A-Z */
          if (sortMode.value === 'name_asc') {
            const nameA =
              getProductName(productA)

            const nameB =
              getProductName(productB)

            return nameA.localeCompare(
              nameB,
              'zh-CN',
              {
                numeric: true,
                sensitivity: 'base',
              },
            )
          }

          /* 更新时间 最新 */
          if (
            sortMode.value ===
            'updated_desc'
          ) {
            const timeA =
              Date.parse(
                productA?.updated_at || '',
              ) || 0

            const timeB =
              Date.parse(
                productB?.updated_at || '',
              ) || 0

            return timeB - timeA
          }

          /* 总库存排序 */
          const totalA =
            productA?.inventory?.total

          const totalB =
            productB?.inventory?.total

          /*
           * null 表示未知。
           * 无论升序还是降序，未知库存都排在最后。
           */
          if (
            totalA == null &&
            totalB == null
          ) {
            return 0
          }

          if (totalA == null) {
            return 1
          }

          if (totalB == null) {
            return -1
          }

          const numberA = Number(totalA)
          const numberB = Number(totalB)

          if (
            Number.isNaN(numberA) &&
            Number.isNaN(numberB)
          ) {
            return 0
          }

          if (Number.isNaN(numberA)) {
            return 1
          }

          if (Number.isNaN(numberB)) {
            return -1
          }

          if (
            sortMode.value ===
            'total_asc'
          ) {
            return numberA - numberB
          }

          return numberB - numberA
        },
      )
    })

    /* ==================== 重置当前页筛选 ==================== */

    const resetPageFilters = () => {
      keyword.value = ''
      inventoryFilter.value = 'all'
      sortMode.value = 'default'
    }

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

        return false
      }

      if (loading.value) {
        return false
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

        /*
         * 返回 true 表示本次商品和库存数据
         * 已经成功从后端获取。
         */
        return true
      } catch (error) {
        products.value = []
        total.value = 0

        errorMessage.value =
          error.userMessage ||
          '商品列表加载失败'

        return false
      } finally {
        loading.value = false
      }
    }

    /* ==================== 主动刷新商品数据 ==================== */

    /*
     * 只有用户主动点击顶部刷新按钮，
     * 并且接口请求成功时才显示成功消息。
     *
     * 首次加载、翻页和改变每页数量仍然直接调用
     * loadProducts，不会重复弹出成功提示。
     */
    const refreshProducts = async () => {
      const succeeded =
        await loadProducts()

      if (!succeeded) {
        return
      }

      message.success(
        '数据刷新成功',
      )
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

    /* ==================== 商品详情弹窗 ==================== */

    const detailModalVisible = ref(false)
    const detailLoading = ref(false)
    const selectedProduct = ref(null)

    /*
     * 商品详情中的全部有效图片。
     * 列表只显示第一张，详情中允许查看全部图片。
     */
    const detailImages = computed(() => {
      const images =
        selectedProduct.value?.images

      if (!Array.isArray(images)) {
        return []
      }

      return images.filter((image) => {
        return (
          typeof image === 'string' &&
          image.trim()
        )
      })
    })

    /* ==================== 打开商品详情 ==================== */

    const openProductDetail = async (
      product,
    ) => {
      if (!canViewProductDetail.value) {
        return
      }

      if (
        !product ||
        detailLoading.value
      ) {
        return
      }

      const customerSku = String(
        product.customer_sku ?? '',
      ).trim()

      if (!customerSku) {
        message.warning(
          '当前商品缺少客户 SKU，无法查询详情',
        )

        return
      }

      detailModalVisible.value = true
      detailLoading.value = true
      selectedProduct.value = null

      try {
        selectedProduct.value =
          await getProductDetailApi(
            customerSku,
          )
      } catch (error) {
        detailModalVisible.value = false

        message.error(
          error.userMessage ||
          '商品详情加载失败',
        )
      } finally {
        detailLoading.value = false
      }
    }

    /* ==================== 关闭商品详情 ==================== */

    const closeProductDetail = () => {
      if (detailLoading.value) {
        return
      }

      detailModalVisible.value = false
    }

    /* ==================== 详情展示格式 ==================== */

    const formatDetailValue = (value) => {
      if (
        value == null ||
        value === ''
      ) {
        return '—'
      }

      return value
    }

    const formatBoolean = (value) => {
      if (value === true) {
        return '是'
      }

      if (value === false) {
        return '否'
      }

      return '—'
    }

    const formatDateTime = (value) => {
      if (!value) {
        return '—'
      }

      const date = new Date(value)

      if (Number.isNaN(date.getTime())) {
        /*
         * 后端字段存在但不是浏览器可解析时间时，
         * 保留后端原始内容，不擅自改写。
         */
        return value
      }

      return date.toLocaleString(
        'zh-CN',
        {
          hour12: false,
        },
      )
    }

    /* ==================== 向模板暴露内容 ==================== */

    return {
      canViewProductList,
      canViewProductDetail,

      products,
      loading,
      errorMessage,
      loadProducts,
      refreshProducts,

      keyword,
      inventoryFilter,
      sortMode,
      sortOptions,
      displayedProducts,
      currentPageInventoryCounts,
      resetPageFilters,

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


      detailModalVisible,
      detailLoading,
      selectedProduct,
      detailImages,
      openProductDetail,
      closeProductDetail,

      formatDetailValue,
      formatBoolean,
      formatDateTime,
    }
  },
}