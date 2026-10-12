/* ==================== Vue 相关依赖 ==================== */

import {
  computed,
} from 'vue'

/* ==================== 公共工具 ==================== */

import { copyText } from '@/utils/clipboard'
import { message } from '@/utils/message'

/* ==================== 公共复制文本组件 ==================== */

export default {
  name: 'AppCopyText',

  props: {
    /*
     * 实际显示和复制的内容。
     *
     * 支持字符串和数字，
     * 数字 0 也是合法复制内容。
     */
    value: {
      type: [
        String,
        Number,
      ],
      default: '',
    },

    /*
     * 内容的业务名称。
     *
     * 例如：
     * 商品名、客户 SKU、ERP SKU、订单号。
     */
    label: {
      type: String,
      default: '内容',
    },

    // 内容为空时显示的占位文本
    emptyText: {
      type: String,
      default: '—',
    },

    /*
     * 自定义成功提示。
     *
     * 未传入时默认显示：
     * 客户 SKU“SET-001”复制成功
     */
    successMessage: {
      type: String,
      default: '',
    },
  },

  emits: [
    'copied',
    'copy-error',
  ],

  setup(props, { emit }) {
    /* ==================== 复制内容 ==================== */

    const normalizedValue = computed(() => {
      return String(
        props.value ?? '',
      ).trim()
    })

    const hasValue = computed(() => {
      return normalizedValue.value !== ''
    })

    const copyTitle = computed(() => {
      return `点击复制${props.label}`
    })

    /* ==================== 执行复制 ==================== */

    const handleCopy = async () => {
      if (!hasValue.value) {
        return
      }

      try {
        const copiedText =
          await copyText(
            normalizedValue.value,
          )

        message.success(
          props.successMessage ||
          `${props.label}“${copiedText}”复制成功`,
        )

        emit('copied', copiedText)
      } catch (error) {
        message.error(
          `${props.label}复制失败，请手动复制`,
        )

        emit('copy-error', error)
      }
    }

    /* ==================== 向模板暴露内容 ==================== */

    return {
      normalizedValue,
      hasValue,
      copyTitle,
      handleCopy,
    }
  },
}