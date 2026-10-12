<!-- ==================== 公共复制文本逻辑 ==================== -->

<script src="./copy-text.js"></script>

<template>
  <!-- ==================== 可复制内容 ==================== -->

  <button
    v-if="hasValue"
    class="app-copy-text"
    type="button"
    :title="copyTitle"
    @click="handleCopy"
  >
    <span>{{ normalizedValue }}</span>

    <i
      class="bi bi-copy"
      aria-hidden="true"
    ></i>
  </button>

  <!-- ==================== 空内容 ==================== -->

  <span
    v-else
    class="app-copy-text-empty"
  >
    {{ emptyText }}
  </span>
</template>

<!-- ==================== 公共复制文本样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./copy-text.scss"
></style>