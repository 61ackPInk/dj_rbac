<!-- ==================== 公共下拉框业务逻辑 ==================== -->

<script src="./app-select.js"></script>

<template>
  <!-- ==================== Element Plus 下拉框 ==================== -->

  <el-select
    class="app-select"
    :style="selectStyle"
    :model-value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :loading="loading"
    :clearable="clearable"
    :filterable="filterable"
    :multiple="multiple"
    :fit-input-width="fitInputWidth"
    :empty-values="emptyValues"
    :value-on-clear="valueOnClear"
    :suffix-icon="SelectChevronIcon"
    popper-class="app-select-popper"
    placement="bottom-start"
    teleported
    @update:model-value="handleUpdate"
    @change="handleChange"
    @clear="handleClear"
    @visible-change="handleVisibleChange"
    @focus="handleFocus"
    @blur="handleBlur"
  >
    <!-- ==================== 下拉选项 ==================== -->

    <el-option
      v-for="option in options"
      :key="String(option.value)"
      :label="option.label"
      :value="option.value"
      :disabled="Boolean(option.disabled)"
    />

    <!-- ==================== 无数据状态 ==================== -->

    <template #empty>
      <div class="app-select-empty">
        <i
          class="bi bi-inbox"
          aria-hidden="true"
        ></i>

        <span>{{ emptyText }}</span>
      </div>
    </template>
  </el-select>
</template>

<!-- ==================== 公共下拉框样式 ==================== -->

<!--
  这里不使用 scoped。

  原因是 Element Plus 会将下拉面板传送到 body 下，
  scoped 样式无法稳定匹配传送后的选项面板。

  app-select.scss 中所有样式均通过
  .app-select 或 .app-select-popper 限制作用范围，
  不会影响其他 Element Plus 组件。
-->
<style
  lang="scss"
  src="./app-select.scss"
></style>