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

      <!-- 显示模式切换 -->

      <div
        v-if="canViewBundleList"
        class="view-switch"
        role="group"
        aria-label="商品组合显示方式"
      >
        <button
          class="view-button"
          :class="{
            'is-active': viewMode === 'list',
          }"
          type="button"
          aria-label="列表显示"
          :aria-pressed="viewMode === 'list'"
          @click="setViewMode('list')"
        >
          <i
            class="bi bi-list-ul"
            aria-hidden="true"
          ></i>
        </button>

        <button
          class="view-button"
          :class="{
            'is-active': viewMode === 'card',
          }"
          type="button"
          aria-label="卡片显示"
          :aria-pressed="viewMode === 'card'"
          @click="setViewMode('card')"
        >
          <i
            class="bi bi-grid"
            aria-hidden="true"
          ></i>
        </button>
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
        <!-- ==================== 当前页即时搜索 ==================== -->

        <div class="bundle-toolbar">
          <label class="search-box">
            <i
              class="bi bi-search"
              aria-hidden="true"
            ></i>

            <input
              v-model="keyword"
              type="search"
              placeholder="搜索组合名称、组合 SKU、子商品名称或子 SKU"
              aria-label="搜索当前页商品组合"
            />
          </label>
        </div>

        <!-- 列表统计 -->

        <header class="bundle-summary">
          <span>
            ERP 共
            <strong>{{ total }}</strong>
            个组合，当前页
            <strong>{{ bundles.length }}</strong>
            个
          </span>

          <span>
            当前搜索结果
            <strong>{{ displayedBundles.length }}</strong>
            个
          </span>
        </header>

        <!-- 当前页无匹配结果 -->

        <div
          v-if="displayedBundles.length === 0"
          class="page-state filtered-empty"
        >
          <i
            class="bi bi-search"
            aria-hidden="true"
          ></i>

          <strong>当前页没有匹配的商品组合</strong>
          <span>
            请修改组合名称、组合 SKU 或子商品搜索内容。
          </span>

          <button
            class="secondary-button"
            type="button"
            @click="clearSearch"
          >
            清除搜索
          </button>
        </div>

        <!-- ==================== 列表显示 ==================== -->

        <div
          v-else-if="viewMode === 'list'"
          class="table-scroll"
        >
          <table class="bundle-table">
            <thead>
              <tr>
                <th>商品组合</th>
                <th>组合 SKU</th>
                <th>状态</th>
                <th>可用数量</th>
                <th>组成商品</th>
                <th>采集时间</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="bundle in displayedBundles"
                :key="bundle.id"
              >
                <td>
                  <div class="bundle-name-cell">
                    <div
                      class="bundle-thumbnail"
                      @click.stop
                      @keydown.stop
                    >
                      <el-image
                        v-if="bundle.image_url"
                        class="bundle-preview-image"
                        :src="bundle.image_url"
                        :preview-src-list="[
                          bundle.image_url,
                        ]"
                        :alt="bundle.name || bundle.bundle_sku"
                        fit="contain"
                        loading="lazy"
                        preview-teleported
                        hide-on-click-modal
                        :infinite="false"
                        :z-index="10000"
                      >
                        <template #error>
                          <i
                            class="bi bi-image"
                            aria-hidden="true"
                          ></i>
                        </template>
                      </el-image>

                      <i
                        v-else
                        class="bi bi-image"
                        aria-hidden="true"
                      ></i>
                    </div>

                    <strong>
                      {{ bundle.name || '未命名组合' }}
                    </strong>
                  </div>
                </td>

                <td class="sku-cell">
                  {{ bundle.bundle_sku || '-' }}
                </td>

                <td>
                  <span class="status-badge">
                    {{
                      bundle.source_status_name ||
                      '状态未知'
                    }}
                  </span>
                </td>

                <td class="quantity-column">
                  {{
                    formatQuantity(
                      bundle.available_quantity,
                    )
                  }}
                </td>

                <td class="quantity-column">
                  {{
                    formatQuantity(
                      bundle.item_count,
                    )
                  }}
                </td>

                <td>
                  {{
                    formatDateTime(
                      bundle.collected_at,
                    )
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- ==================== 卡片显示 ==================== -->

        <div
          v-else
          class="bundle-card-view"
        >
          <article
            v-for="bundle in displayedBundles"
            :key="bundle.id"
            class="bundle-card"
          >
            <div
              class="bundle-card-image"
              @click.stop
              @keydown.stop
            >
              <el-image
                v-if="bundle.image_url"
                class="bundle-preview-image"
                :src="bundle.image_url"
                :preview-src-list="[
                  bundle.image_url,
                ]"
                :alt="bundle.name || bundle.bundle_sku"
                fit="contain"
                loading="lazy"
                preview-teleported
                hide-on-click-modal
                :infinite="false"
                :z-index="10000"
              >
                <template #error>
                  <div class="image-placeholder">
                    <i
                      class="bi bi-image"
                      aria-hidden="true"
                    ></i>
                    <span>暂无组合图片</span>
                  </div>
                </template>
              </el-image>

              <div
                v-else
                class="image-placeholder"
              >
                <i
                  class="bi bi-image"
                  aria-hidden="true"
                ></i>
                <span>暂无组合图片</span>
              </div>
            </div>

            <div class="bundle-card-content">
              <div class="bundle-card-title">
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

              <div class="bundle-card-sku">
                {{ bundle.bundle_sku || '-' }}
              </div>

              <dl class="bundle-card-meta">
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
              </dl>

              <div class="bundle-card-time">
                <i
                  class="bi bi-clock"
                  aria-hidden="true"
                ></i>
                {{
                  formatDateTime(
                    bundle.collected_at,
                  )
                }}
              </div>
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
