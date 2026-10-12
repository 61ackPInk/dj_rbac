/* ==================== 兼容复制方法 ==================== */

/*
 * navigator.clipboard 通常只在 HTTPS 或 localhost 下可用。
 *
 * 当前项目还可能通过局域网 HTTP 地址访问，
 * 因此保留 textarea 复制作为兼容方案。
 */
const copyTextWithFallback = (text) => {
  const textarea =
    document.createElement('textarea')

  textarea.value = text
  textarea.setAttribute(
    'readonly',
    '',
  )

  /*
   * 元素需要加入页面才能被选中，
   * 但不能影响现有页面布局。
   */
  textarea.style.position = 'fixed'
  textarea.style.left = '-9999px'
  textarea.style.opacity = '0'
  textarea.style.pointerEvents = 'none'

  document.body.appendChild(textarea)
  textarea.select()

  try {
    const copied =
      document.execCommand('copy')

    if (!copied) {
      throw new Error('复制命令执行失败')
    }
  } finally {
    document.body.removeChild(textarea)
  }
}

/* ==================== 公共复制方法 ==================== */

/*
 * 将指定内容写入系统剪贴板。
 *
 * 成功时正常 resolve；
 * 内容为空或复制失败时抛出错误，
 * 由调用方决定显示什么提示。
 */
export const copyText = async (value) => {
  const text = String(
    value ?? '',
  ).trim()

  if (!text) {
    throw new Error('没有可复制的内容')
  }

  /*
   * 安全环境优先使用现代 Clipboard API。
   */
  if (
    navigator.clipboard &&
    window.isSecureContext
  ) {
    try {
      await navigator.clipboard.writeText(
        text,
      )

      return text
    } catch {
      /*
       * 浏览器可能拒绝剪贴板权限，
       * 此时继续尝试兼容方法。
       */
    }
  }

  copyTextWithFallback(text)

  return text
}