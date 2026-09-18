import { defineComponent } from 'vue'
import { message, messageState } from '@/utils/message'

export default defineComponent({
  name: 'AppMessage',

  setup() {
    // 使用已安装的 bootstrap-icons，不增加依赖
    const icons = {
      success: 'bi-check-circle-fill',
      error: 'bi-x-circle-fill',
      warning: 'bi-exclamation-triangle-fill',
      info: 'bi-info-circle-fill',
    }

    const closeMessage = (id) => {
      message.close(id)
    }

    return {
      messageState,
      icons,
      closeMessage,
    }
  },
})