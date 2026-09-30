/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
} from 'vue'

/* ==================== 公共操作菜单组件 ==================== */

export default {
  name: 'AppActionMenu',

  /* ==================== 组件参数 ==================== */

  props: {
    /*
     * 操作选项。
     *
     * 标准格式：
     * [
     *   {
     *     key: 'detail',
     *     label: '查看详情',
     *     icon: 'bi bi-eye',
     *     danger: false,
     *     disabled: false,
     *   },
     * ]
     */
    items: {
      type: Array,
      default: () => [],
    },

    /*
     * 菜单触发按钮的辅助说明。
     * 主要供无障碍功能使用。
     */
    ariaLabel: {
      type: String,
      default: '打开操作菜单',
    },

    /*
     * 整个操作菜单是否禁用。
     */
    disabled: {
      type: Boolean,
      default: false,
    },
  },

  /* ==================== 组件事件 ==================== */

  emits: [
    'select',
  ],

  setup(props, { emit }) {
    /* ==================== 有效操作选项 ==================== */

    /*
     * visible 明确等于 false 时隐藏。
     *
     * 页面可以通过它控制权限：
     * {
     *   key: 'edit',
     *   visible: canEditRole,
     * }
     */
    const visibleItems = computed(() =>
      props.items.filter(
        (item) => item && item.visible !== false,
      ),
    )

    /* ==================== 选择操作 ==================== */

    const handleCommand = (command) => {
      const selectedItem = visibleItems.value.find(
        (item) => item.key === command,
      )

      if (!selectedItem || selectedItem.disabled) {
        return
      }

      /*
       * 同时返回操作标识和完整选项，
       * 父页面可以根据 key 执行对应功能。
       */
      emit('select', command, selectedItem)
    }

    /* ==================== 暴露给模板 ==================== */

    return {
      visibleItems,
      handleCommand,
    }
  },
}