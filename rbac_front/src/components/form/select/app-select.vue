<!-- ==================== 公共下拉框业务逻辑 ==================== -->

<script src="./app-select.js"></script>

<template>
  <!-- ==================== Element Plus 下拉框 ==================== -->

  <el-select
    class="app-select"
    :style="selectStyle"
    :model-value="selectModelValue"
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

    <!-- ==================== 当前选中项图标 ==================== -->

    <!--
    普通选项没有 icon 时不显示任何内容。
    页面图标选项存在 icon 时显示 Bootstrap Icon。
    -->
    <template
    v-if="selectedOption?.icon"
    #prefix
    >
    <i
        :class="[
        selectedOption.icon,
        'app-select__selected-icon',
        ]"
        aria-hidden="true"
    ></i>
    </template>

    <!-- ==================== 下拉选项 ==================== -->

    <el-option
        v-for="option in normalizedOptions"
        :key="option.appSelectKey"
        :label="option.label"
        :value="option.appSelectValue"
        :disabled="Boolean(option.disabled)"
    >
    <!-- ==================== 自定义选项内容 ==================== -->

        <div class="app-select-option">
            <!-- Bootstrap 图标 -->
            <span
                v-if="option.icon"
                class="app-select-option__icon"
                aria-hidden="true"
            >
            <i :class="option.icon"></i>
            </span>

            <!-- 选项名称 -->
            <span class="app-select-option__label">
                {{ option.label }}
            </span>

            <!-- 可选说明 -->
            <small
                v-if="option.description"
                class="app-select-option__description"
                >
                {{ option.description }}
            </small>
        </div>
    </el-option>

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