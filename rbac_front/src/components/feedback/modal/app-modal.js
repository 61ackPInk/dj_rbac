/* ==================== Vue 相关依赖 ==================== */
import {
  computed,
  defineComponent,
  nextTick,
  onBeforeUnmount,
  ref,
  watch,
} from 'vue'

/* ==================== 页面滚动锁定状态 ==================== */

/*
 * 记录当前打开的公共弹出层数量。
 *
 * 后续如果出现弹出层嵌套，可以避免关闭其中一个弹出层时，
 * 错误地恢复页面滚动。
 */
let openedModalCount = 0

/*
 * 保存弹出层打开前 body 原来的 overflow。
 */
let originalBodyOverflow = ''

/* ==================== 页面滚动控制 ==================== */

const lockBodyScroll = () => {
  if (openedModalCount === 0) {
    originalBodyOverflow =
      document.body.style.overflow

    document.body.style.overflow = 'hidden'
  }

  openedModalCount += 1
}

const unlockBodyScroll = () => {
  openedModalCount = Math.max(
    openedModalCount - 1,
    0,
  )

  if (openedModalCount === 0) {
    document.body.style.overflow =
      originalBodyOverflow

    originalBodyOverflow = ''
  }
}

export default defineComponent({
  name: 'AppModal',

  /* ==================== 组件参数 ==================== */

  props: {
    /*
     * 控制弹出层是否打开。
     *
     * 使用方式：
     * v-model="modalVisible"
     */
    modelValue: {
      type: Boolean,
      default: false,
    },

    // 弹出层标题
    title: {
      type: String,
      default: '',
    },

    /*
     * 弹出层宽度。
     *
     * 可以传入数字：
     * :width="560"
     *
     * 也可以传入字符串：
     * width="720px"
     * width="60vw"
     */
    width: {
      type: [Number, String],
      default: 560,
    },

    // 是否显示右上角关闭按钮
    showClose: {
      type: Boolean,
      default: true,
    },

    // 点击遮罩是否允许关闭
    closeOnOverlay: {
      type: Boolean,
      default: true,
    },

    // 按下 Esc 是否允许关闭
    closeOnEscape: {
      type: Boolean,
      default: true,
    },

    /*
     * 是否允许关闭弹出层。
     *
     * 提交表单时可以设置为 false，
     * 防止请求进行过程中误关弹出层。
     */
    closable: {
      type: Boolean,
      default: true,
    },
  },

  /* ==================== 组件事件 ==================== */

  emits: [
    'update:modelValue',
    'close',
  ],

  setup(props, { emit }) {
    /* ==================== 元素引用 ==================== */

    // 弹出层主体元素
    const dialogRef = ref(null)

    /*
     * 记录打开弹出层前获得焦点的元素，
     * 关闭后将焦点还给它。
     */
    let previousActiveElement = null

    /*
     * 记录当前组件是否已经执行过滚动锁定，
     * 防止重复增加 openedModalCount。
     */
    let bodyScrollLocked = false

    /* ==================== 弹出层宽度 ==================== */

    const modalWidth = computed(() => {
      if (typeof props.width === 'number') {
        return `${props.width}px`
      }

      return props.width
    })

    /*
     * 使用 CSS 变量把宽度传给样式文件。
     */
    const modalStyle = computed(() => {
      return {
        '--app-modal-width': modalWidth.value,
      }
    })

    /* ==================== 打开弹出层 ==================== */

    const handleOpen = async () => {
      previousActiveElement =
        document.activeElement

      if (!bodyScrollLocked) {
        lockBodyScroll()
        bodyScrollLocked = true
      }

      /*
       * 等待弹出层完成渲染后，
       * 将焦点移动到弹出层主体。
       */
      await nextTick()

      dialogRef.value?.focus()
    }

    /* ==================== 关闭后的清理 ==================== */

    const handleClosed = () => {
      if (bodyScrollLocked) {
        unlockBodyScroll()
        bodyScrollLocked = false
      }

      /*
       * 弹出层关闭后，
       * 将焦点还给打开它的按钮。
       */
      if (
        previousActiveElement instanceof
        HTMLElement
      ) {
        previousActiveElement.focus()
      }

      previousActiveElement = null
    }

    /* ==================== 请求关闭弹出层 ==================== */

    /*
     * reason 用于告诉父组件弹出层通过什么方式关闭：
     *
     * close-button：点击右上角关闭按钮
     * overlay：点击遮罩
     * escape：按下 Esc
     * programmatic：父组件主动关闭
     */
    const requestClose = (reason) => {
      if (!props.closable) {
        return
      }

      emit('update:modelValue', false)
      emit('close', reason)
    }

    /* ==================== 关闭按钮 ==================== */

    const handleCloseButton = () => {
      requestClose('close-button')
    }

    /* ==================== 遮罩点击 ==================== */

    const handleOverlayClick = () => {
      if (!props.closeOnOverlay) {
        return
      }

      requestClose('overlay')
    }

    /* ==================== 键盘操作 ==================== */

    const handleKeydown = (event) => {
      if (
        event.key !== 'Escape' ||
        !props.modelValue ||
        !props.closeOnEscape
      ) {
        return
      }

      requestClose('escape')
    }

    /* ==================== 监听打开状态 ==================== */

    watch(
      () => props.modelValue,
      (visible) => {
        if (visible) {
          handleOpen()
          return
        }

        handleClosed()
      },
    )

    /* ==================== 组件销毁清理 ==================== */

    onBeforeUnmount(() => {
      if (bodyScrollLocked) {
        unlockBodyScroll()
        bodyScrollLocked = false
      }
    })

    /* ==================== 向模板暴露内容 ==================== */

    return {
      dialogRef,
      modalStyle,

      handleCloseButton,
      handleOverlayClick,
      handleKeydown,
    }
  },
})