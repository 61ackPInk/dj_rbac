import { defineComponent } from 'vue'
import { message } from '@/utils/message'

export default defineComponent({
  name: 'TestView',

  setup() {
    const showSuccess = () => {
      message.success('操作成功，信息已保存')
    }

    const showError = () => {
      message.error('操作失败，请稍后重试')
    }

    const showWarning = () => {
      message.warning('请先填写完整信息')
    }

    const showInfo = () => {
      message.info('这是一条普通提示')
    }

    const showLongText = () => {
      message.info(
        '这是一条较长的提示信息，用于检查文字换行、提示框最大宽度，以及手机屏幕上的显示效果。',
        { duration: 5000 },
      )
    }

    const showPersistent = () => {
      // 不自动关闭，点击提示右侧关闭按钮即可关闭
      message.info('这条提示不会自动关闭', {
        duration: 0,
      })
    }

    const closeAll = () => {
      message.closeAll()
    }

    // 模板需要使用的方法都在这里返回
    return {
      showSuccess,
      showError,
      showWarning,
      showInfo,
      showLongText,
      showPersistent,
      closeAll,
    }
  },
})