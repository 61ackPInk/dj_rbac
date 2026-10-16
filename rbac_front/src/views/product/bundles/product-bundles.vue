<!-- ==================== 商品组合业务逻辑 ==================== -->

<script src="./product-bundles.js"></script>

<template>
  <div class="product-bundles-page">
    <!-- ==================== 页面标题 ==================== -->

    <header class="page-heading">
      <div>
        <h1>商品组合</h1>
        <p>
          查看不同仓库中的商品组合及组成商品明细。
        </p>
      </div>
    </header>

    <!-- ==================== 仓库选择面板 ==================== -->

    <section class="warehouse-panel">
      <!-- 无操作权限 -->

      <div
        v-if="!canViewBundleList"
        class="page-state"
        role="alert"
      >
        <i
          class="bi bi-shield-lock"
          aria-hidden="true"
        ></i>

        <strong>无法查看商品组合</strong>
        <span>
          当前用户没有 PRODUCT_BUNDLE_LIST 操作权限。
        </span>
      </div>

      <template v-else>
        <div class="warehouse-field">
          <label for="bundle-warehouse">
            仓库
          </label>

          <AppSelect
            id="bundle-warehouse"
            v-model="warehouseCode"
            :options="warehouseOptions"
            :placeholder="warehousePlaceholder"
            :loading="warehouseLoading"
            :disabled="
              warehouseLoading ||
              warehouses.length === 0
            "
            empty-text="暂无可用仓库"
            width="280px"
            @change="handleWarehouseChange"
          />
        </div>

        <!-- 仓库加载错误 -->

        <div
          v-if="warehouseError"
          class="page-state error"
          role="alert"
        >
          <i
            class="bi bi-exclamation-circle"
            aria-hidden="true"
          ></i>

          <strong>仓库列表加载失败</strong>
          <span>{{ warehouseError }}</span>

          <button
            class="secondary-button"
            type="button"
            @click="loadWarehouses"
          >
            重新加载
          </button>
        </div>

        <!-- 仓库为空 -->

        <div
          v-else-if="
            !warehouseLoading &&
            warehouses.length === 0
          "
          class="page-state"
        >
          <i
            class="bi bi-building"
            aria-hidden="true"
          ></i>

          <strong>暂无可用仓库</strong>
          <span>
            ERP 当前没有返回可以选择的仓库。
          </span>
        </div>
      </template>
    </section>
  </div>
</template>

<style
  src="./product-bundles.scss"
  lang="scss"
  scoped
></style>