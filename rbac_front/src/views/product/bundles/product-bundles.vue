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

    <!-- ==================== 商品组合列表 ==================== -->

    <section
      v-if="
        canViewBundleList &&
        warehouseCode &&
        !warehouseError
      "
      class="bundle-panel"
    >
      <!-- 组合列表加载状态 -->

      <div
        v-if="
          bundleLoading &&
          bundles.length === 0
        "
        class="page-state"
      >
        <i
          class="bi bi-arrow-clockwise is-rotating"
          aria-hidden="true"
        ></i>

        <strong>正在读取商品组合</strong>
        <span>
          正在从 ERP 获取当前仓库的商品组合。
        </span>
      </div>

      <!-- 组合列表错误 -->

      <div
        v-else-if="bundleError"
        class="page-state error"
        role="alert"
      >
        <i
          class="bi bi-exclamation-circle"
          aria-hidden="true"
        ></i>

        <strong>商品组合加载失败</strong>
        <span>{{ bundleError }}</span>

        <button
          class="secondary-button"
          type="button"
          @click="loadBundles"
        >
          重新加载
        </button>
      </div>

      <!-- 组合列表为空 -->

      <div
        v-else-if="bundles.length === 0"
        class="page-state"
      >
        <i
          class="bi bi-boxes"
          aria-hidden="true"
        ></i>

        <strong>暂无商品组合</strong>
        <span>
          当前仓库没有可显示的商品组合。
        </span>
      </div>

      <template v-else>
        <!-- 列表统计 -->

        <header class="bundle-summary">
          <span>
            共 {{ total }} 个商品组合
          </span>

          <span>
            当前仓库：{{ warehouseCode }}
          </span>
        </header>

        <!-- 组合列表 -->

        <div class="bundle-list">
          <article
            v-for="bundle in bundles"
            :key="bundle.id"
            class="bundle-item"
          >
            <div class="bundle-image">
              <img
                v-if="bundle.image_url"
                :src="bundle.image_url"
                :alt="bundle.name || bundle.bundle_sku"
                loading="lazy"
              />

              <i
                v-else
                class="bi bi-image"
                aria-hidden="true"
              ></i>
            </div>

            <div class="bundle-main">
              <div class="bundle-title">
                <strong>
                  {{ bundle.name || '未命名组合' }}
                </strong>

                <span class="status-badge">
                  {{
                    bundle.source_status_name ||
                    '状态未知'
                  }}
                </span>
              </div>

              <dl class="bundle-meta">
                <div>
                  <dt>组合 SKU</dt>
                  <dd>
                    {{ bundle.bundle_sku || '-' }}
                  </dd>
                </div>

                <div>
                  <dt>可用数量</dt>
                  <dd>
                    {{
                      formatQuantity(
                        bundle.available_quantity,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>组成商品</dt>
                  <dd>
                    {{
                      formatQuantity(
                        bundle.item_count,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>采集时间</dt>
                  <dd>
                    {{
                      formatDateTime(
                        bundle.collected_at,
                      )
                    }}
                  </dd>
                </div>
              </dl>
            </div>
          </article>
        </div>

        <!-- 后端分页 -->

        <footer class="pagination-bar">
          <AppSelect
            v-model="pageSize"
            :options="pageSizeOptions"
            :width="132"
            aria-label="每页商品组合数量"
            @change="changePageSize"
          />

          <div class="pagination-controls">
            <button
              type="button"
              :disabled="
                bundleLoading ||
                !canGoPrevious
              "
              aria-label="上一页"
              @click="goToPreviousPage"
            >
              <i
                class="bi bi-chevron-left"
                aria-hidden="true"
              ></i>
            </button>

            <span>
              第 {{ page }} / {{ totalPages }} 页
            </span>

            <button
              type="button"
              :disabled="
                bundleLoading ||
                !canGoNext
              "
              aria-label="下一页"
              @click="goToNextPage"
            >
              <i
                class="bi bi-chevron-right"
                aria-hidden="true"
              ></i>
            </button>
          </div>
        </footer>
      </template>
    </section>
  </div>
</template>

<style
  src="./product-bundles.scss"
  lang="scss"
  scoped
></style>
