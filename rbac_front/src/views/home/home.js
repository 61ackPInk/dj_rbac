/* ==================== Vue 相关依赖 ==================== */
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'HomeView',

  setup() {
    /*
     * 当前首页只负责展示工作台卡片。
     *
     * 后续卡片接入真实数据时，
     * 再在这里增加接口调用、加载状态和数据处理。
     */

    /* ==================== 向模板暴露内容 ==================== */

    return {}
  },
})