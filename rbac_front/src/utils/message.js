import { reactive } from 'vue'

// 所有页面与提示组件共用同一份状态
const state = reactive({
  messages: [],
})

const timers = new Map()
let nextId = 0

export const messageState = state

const closeMessage = (id) => {
  const timer = timers.get(id)

  if (timer !== undefined) {
    window.clearTimeout(timer)
    timers.delete(id)
  }

  const index = state.messages.findIndex((item) => item.id === id)

  if (index !== -1) {
    state.messages.splice(index, 1)
  }
}

const showMessage = (type, text, options = {}) => {
  const content = String(text ?? '')
  if (!content.trim()) return null

  const duration = options.duration ?? 3000
  const id = ++nextId

  // 最多保留 5 条，避免提示占满屏幕
  if (state.messages.length >= 5) {
    closeMessage(state.messages[0].id)
  }

  state.messages.push({
    id,
    type,
    text: content,
    closable: options.closable ?? true,
  })

  // duration 为 0 时不自动关闭
  if (duration > 0) {
    const timer = window.setTimeout(() => {
      closeMessage(id)
    }, duration)

    timers.set(id, timer)
  }

  // 返回关闭方法，适合“不自动关闭”的提示
  return {
    close: () => closeMessage(id),
  }
}

const closeAll = () => {
  /*
   * 先复制 ID，再逐条关闭。
   * closeMessage 会删除原数组内容，
   * 不直接遍历正在被修改的原数组。
   */
  const ids = state.messages.map((item) => item.id)
  ids.forEach(closeMessage)
}

export const message = {
  success: (text, options) => showMessage('success', text, options),
  error: (text, options) => showMessage('error', text, options),
  warning: (text, options) => showMessage('warning', text, options),
  info: (text, options) => showMessage('info', text, options),
  close: closeMessage,
  closeAll,
}