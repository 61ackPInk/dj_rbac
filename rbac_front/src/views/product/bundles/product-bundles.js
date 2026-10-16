/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
  onMounted,
  ref,
} from 'vue'

/* ==================== 公共组件 ==================== */

import AppSelect from '@/components/form/select/app-select.vue'

/* ==================== 商品组合接口与权限 ==================== */

import {
  getProductWarehousesApi,
} from '@/api/product-bundles'
import { useAuthStore } from '@/stores/auth'

/* ==================== 商品组合页面 ==================== */

export default {
  name: 'ProductBundlesView',

  components: {
    AppSelect,
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
          label: warehouse.name,
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

    /* ==================== 组合分页状态 ==================== */

    /*
     * 下一步接入组合列表时直接使用。
     * 切换仓库必须回到第一页。
     */
    const page = ref(1)

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
        } else {
          warehouseCode.value = undefined
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

      /*
       * 下一步在这里调用组合列表接口。
       * 当前步骤只维护仓库和分页状态。
       */
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

      loadWarehouses,
      handleWarehouseChange,
    }
  },
}