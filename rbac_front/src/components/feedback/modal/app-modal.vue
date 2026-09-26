<!-- ==================== 弹出层业务逻辑 ==================== -->
<script src="./app-modal.js"></script>

<template>
  <!--
    将弹出层移动到 body 下。
    避免受到页面容器的 overflow、z-index 和 transform 影响。
  -->
  <Teleport to="body">
    <!-- ==================== 弹出层过渡动画 ==================== -->
    <Transition name="app-modal">
      <!-- ==================== 弹出层遮罩 ==================== -->
      <div
        v-if="modelValue"
        class="app-modal-overlay"
        @mousedown.self="handleOverlayClick"
        @keydown="handleKeydown"
      >
        <!-- ==================== 弹出层主体 ==================== -->
        <section
          ref="dialogRef"
          class="app-modal-dialog"
          :style="modalStyle"
          role="dialog"
          aria-modal="true"
          :aria-label="title || '弹出层'"
          tabindex="-1"
        >
          <!-- ==================== 弹出层头部 ==================== -->
          <header
            v-if="title || $slots.title || showClose"
            class="app-modal-header"
          >
            <!--
              标题插槽：
              父组件需要自定义标题结构时可以使用。
              没有传入标题插槽时显示 title 属性。
            -->
            <div class="app-modal-title">
              <slot name="title">
                <h2>{{ title }}</h2>
              </slot>
            </div>

            <!-- 右上角关闭按钮 -->
            <button
              v-if="showClose"
              class="app-modal-close"
              type="button"
              aria-label="关闭弹出层"
              :disabled="!closable"
              @click="handleCloseButton"
            >
              <i
                class="bi bi-x-lg"
                aria-hidden="true"
              ></i>
            </button>
          </header>

          <!-- ==================== 弹出层内容 ==================== -->
          <div class="app-modal-body">
            <!--
              默认插槽：
              创建用户表单、用户信息等主要内容放在这里。
            -->
            <slot></slot>
          </div>

          <!-- ==================== 弹出层底部 ==================== -->
          <footer
            v-if="$slots.footer"
            class="app-modal-footer"
          >
            <!--
              底部插槽：
              取消、保存、确认等操作按钮放在这里。
            -->
            <slot name="footer"></slot>
          </footer>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<!-- ==================== 弹出层样式 ==================== -->
<style
  scoped
  lang="scss"
  src="./app-modal.scss"
></style>

<!-- 
Teleport
└── app-modal-overlay
    └── app-modal-dialog
        ├── app-modal-header
        │   ├── title 插槽
        │   └── 关闭按钮
        ├── app-modal-body
        │   └── 默认插槽
        └── app-modal-footer
            └── footer 插槽
-->