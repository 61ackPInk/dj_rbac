import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { getVisiblePagesApi } from '@/api/pages'


export const useNavigationStore = defineStore('navigation', () => {

    // ============ State(状态) ============
    const pages = ref([])
    const loading = ref(false)
    const loaded = ref(false)

    // ============ Actions(方法) ============


    // 把页面列表按 sort_order 从小到大排好序
    const sortedPages = computed(() =>
        [...pages.value].sort(
            (a, b) => a.sort_order - b.sort_order,
        ),
    )

    // 挑出所有顶级菜单(没有父级的那种)
    const topMenus = computed(() =>
        sortedPages.value.filter(
            (page) => page.parent_id == null,
        ),
    )

    // 传入一个父级 ID,把这个父级下面所有的子菜单都找出来
    const getChildMenus = (parentId) =>
        sortedPages.value.filter(
            (page) => page.parent_id === parentId,
        )

    // 加载页面列表数据
    const loadPages = async () => {
        // 短路守卫:如果已经加载过(loaded)或正在加载中(loading),直接返回
        // 作用:① 缓存命中的情况下不重复请求 ② 防止并发重复触发
        if (loaded.value || loading.value) return

        // 标记进入加载中状态
        loading.value = true

        try {
            // 调用 API 异步获取页面数据
            const result = await getVisiblePagesApi()
            // 将结果写入响应式状态
            pages.value = result
            // 标记已加载完成,后续调用会命中缓存
            loaded.value = true
        } finally {
            // 无论成功还是失败,都复位加载状态,避免状态卡死
            loading.value = false
        }
    }

    // 清空页面数据并重置加载标记
    // 使用场景:用户登出、权限变更、需要强制刷新数据时调用
    const clearPages = () => {
        // 清空页面列表
        pages.value = []
        // 重置已加载标记,下次调用 loadPages 时会重新请求
        loaded.value = false
    }

    // ============ 对外暴露 ============

    return {
        pages,
        loading,
        loaded,
        topMenus,
        getChildMenus,
        loadPages,
        clearPages,
    }
})