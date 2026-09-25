<script src="./message.js"></script>

<template>
  <!-- 放到 body 下，避免被页面容器的 overflow 裁剪 -->
  <Teleport to="body">
    <div class="app-message-container">
      <TransitionGroup name="app-message" tag="div" class="app-message-list">
        <!--
          每条提示循环渲染一次。
          key 使用唯一 ID，确保动画和关闭操作对应正确的提示。
        -->
        <div
          v-for="item in messageState.messages"
          :key="item.id"
          class="app-message-item"
          :class="`app-message-item--${item.type}`"
          :role="item.type === 'error' ? 'alert' : 'status'"
          aria-atomic="true"
        >
          <i
            class="bi app-message-icon"
            :class="icons[item.type]"
            aria-hidden="true"
          ></i>

          <!-- 使用文本插值，不渲染 HTML，避免不可信内容注入 -->
          <span class="app-message-text">{{ item.text }}</span>

          <button
            v-if="item.closable"
            type="button"
            class="app-message-close"
            aria-label="关闭提示"
            @click="closeMessage(item.id)"
          >
            <i class="bi bi-x-lg" aria-hidden="true"></i>
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped lang="scss" src="./message.scss"></style>