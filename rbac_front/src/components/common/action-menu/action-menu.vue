<!-- ==================== 公共操作菜单逻辑 ==================== -->

<script src="./action-menu.js"></script>

<template>
  <!-- ==================== 行操作下拉菜单 ==================== -->

  <el-dropdown
    v-if="visibleItems.length"
    class="app-action-menu"
    placement="bottom-end"
    trigger="click"
    popper-class="app-action-menu-popper"
    :disabled="disabled"
    :hide-on-click="true"
    :teleported="true"
    @command="handleCommand"
  >
    <!-- ==================== 菜单触发按钮 ==================== -->

    <button
      class="app-action-menu__trigger"
      type="button"
      :disabled="disabled"
      :aria-label="ariaLabel"
      title="更多操作"
      @click.stop
    >
      <i
        class="bi bi-three-dots"
        aria-hidden="true"
      ></i>
    </button>

    <!-- ==================== 菜单选项 ==================== -->

    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item
          v-for="item in visibleItems"
          :key="item.key"
          :command="item.key"
          :disabled="Boolean(item.disabled)"
          :class="{
            'is-danger': item.danger,
          }"
        >
          <!-- 操作图标 -->
          <i
            v-if="item.icon"
            :class="item.icon"
            aria-hidden="true"
          ></i>

          <!-- 操作名称 -->
          <span>{{ item.label }}</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<!--
  这里不能使用 scoped。

  Element Plus 会把菜单面板传送到 body，
  scoped 样式无法匹配传送后的内容。

  所有样式都通过 app-action-menu
  和 app-action-menu-popper 限制作用范围。
-->
<style
  lang="scss"
  src="./action-menu.scss"
></style>