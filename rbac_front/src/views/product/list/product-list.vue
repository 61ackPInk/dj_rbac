<!-- ==================== 商品列表业务逻辑 ==================== -->

<script src="./product-list.js"></script>

<template>
  <div class="product-list-page">
    <!-- ==================== 页面标题 ==================== -->

    <header class="page-heading">
      <div>
        <h1>商品列表</h1>
        <p>查看 ERP 商品资料及实时库存信息。</p>
      </div>

      <div
        v-if="canViewProductList"
        class="heading-actions"
      >
        <!-- 刷新商品列表 -->
        <button
          class="refresh-button"
          type="button"
          :disabled="loading"
          aria-label="刷新商品列表"
          title="刷新商品列表"
          @click="refreshProducts"
        >
          <i
            class="bi bi-arrow-clockwise"
            :class="{
              'is-rotating': loading,
            }"
            aria-hidden="true"
          ></i>
        </button>

        <!-- 显示模式切换 -->
        <div
          class="view-switch"
          role="group"
          aria-label="商品显示方式"
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
      </div>
    </header>

    <!-- ==================== 商品列表面板 ==================== -->

    <section class="product-panel">
      <!-- ==================== 无操作权限 ==================== -->

      <div
        v-if="!canViewProductList"
        class="page-state"
        role="alert"
      >
        <i
          class="bi bi-shield-lock"
          aria-hidden="true"
        ></i>

        <strong>无法查看商品列表</strong>
        <span>
          当前用户没有查看商品列表的操作权限。
        </span>
      </div>

      <!-- ==================== 首次加载 ==================== -->

      <div
        v-else-if="
          loading &&
          products.length === 0
        "
        class="page-state"
      >
        <i
          class="bi bi-arrow-clockwise is-rotating"
          aria-hidden="true"
        ></i>

        <strong>正在读取商品数据</strong>
        <span>
          商品和库存数据正在从 ERP 实时获取。
        </span>
      </div>

      <!-- ==================== 加载错误 ==================== -->

      <div
        v-else-if="errorMessage"
        class="page-state error"
        role="alert"
      >
        <i
          class="bi bi-exclamation-circle"
          aria-hidden="true"
        ></i>

        <strong>商品数据加载失败</strong>
        <span>{{ errorMessage }}</span>

        <button
          class="secondary-button"
          type="button"
          @click="loadProducts"
        >
          重新加载
        </button>
      </div>

      <!-- ==================== 空数据 ==================== -->

      <div
        v-else-if="products.length === 0"
        class="page-state"
      >
        <i
          class="bi bi-box-seam"
          aria-hidden="true"
        ></i>

        <strong>暂无商品数据</strong>
        <span>ERP 当前没有返回商品记录。</span>
      </div>

      <!-- ==================== 商品数据 ==================== -->

      <template v-else>
        <!-- ==================== 当前页搜索与筛选 ==================== -->

        <div class="product-toolbar">
          <!-- 商品搜索 -->
          <label class="search-box">
            <i
              class="bi bi-search"
              aria-hidden="true"
            ></i>

            <input
              v-model="keyword"
              type="search"
              placeholder="搜索商品名称、Customer SKU、ERP SKU"
              aria-label="搜索当前页商品"
            />
          </label>

          <!-- 库存状态筛选 -->
          <div
            class="inventory-filters"
            role="group"
            aria-label="按库存状态筛选当前页商品"
          >
            <button
              type="button"
              :class="{
                'is-active':
                  inventoryFilter === 'all',
              }"
              @click="inventoryFilter = 'all'"
            >
              全部
              <span>
                {{ currentPageInventoryCounts.all }}
              </span>
            </button>

            <button
              type="button"
              :class="{
                'is-active':
                  inventoryFilter === 'in_stock',
              }"
              @click="
                inventoryFilter = 'in_stock'
              "
            >
              有货
              <span>
                {{
                  currentPageInventoryCounts.in_stock
                }}
              </span>
            </button>

            <button
              type="button"
              :class="{
                'is-active':
                  inventoryFilter === 'low_stock',
              }"
              @click="
                inventoryFilter = 'low_stock'
              "
            >
              低库存
              <span>
                {{
                  currentPageInventoryCounts.low_stock
                }}
              </span>
            </button>

            <button
              type="button"
              :class="{
                'is-active':
                  inventoryFilter ===
                  'out_of_stock',
              }"
              @click="
                inventoryFilter = 'out_of_stock'
              "
            >
              无库存
              <span>
                {{
                  currentPageInventoryCounts
                    .out_of_stock
                }}
              </span>
            </button>

            <button
              type="button"
              :class="{
                'is-active':
                  inventoryFilter === 'unknown',
              }"
              @click="
                inventoryFilter = 'unknown'
              "
            >
              未知
              <span>
                {{
                  currentPageInventoryCounts.unknown
                }}
              </span>
            </button>
          </div>

          <!-- 当前页排序 -->
          <div class="sort-control">
            <span>排序</span>

            <AppSelect
              v-model="sortMode"
              :options="sortOptions"
              :width="168"
              aria-label="当前页商品排序"
            />
          </div>
        </div>

        <!-- ==================== 结果统计 ==================== -->

        <div class="result-summary">
          <span>
            ERP 共
            <strong>{{ total }}</strong>
            件商品，当前页
            <strong>{{ products.length }}</strong>
            件
          </span>

          <span>
            当前筛选结果
            <strong>
              {{ displayedProducts.length }}
            </strong>
            件
          </span>
        </div>
        
        <!-- ==================== 当前页无匹配结果 ==================== -->

        <div
          v-if="displayedProducts.length === 0"
          class="page-state filtered-empty"
        >
          <i
            class="bi bi-search"
            aria-hidden="true"
          ></i>

          <strong>当前页没有匹配商品</strong>

          <span>
            请修改搜索内容或库存状态筛选。
          </span>

          <button
            class="secondary-button"
            type="button"
            @click="resetPageFilters"
          >
            清除筛选
          </button>
        </div>

        <!-- ==================== 列表显示 ==================== -->

        <div
          v-else-if="viewMode === 'list'"
          class="table-scroll"
        >
          <table class="product-table">
            <thead>
              <tr>
                <th>商品</th>
                <th>客户 SKU</th>
                <th>ERP SKU</th>
                <th>主仓库</th>
                <th>商品状态</th>
                <th>库存状态</th>
                <th class="quantity-column">
                  总库存
                </th>
                <th class="quantity-column">
                  可用库存
                </th>
                <th class="quantity-column">
                  在途
                </th>
                <th class="quantity-column">
                  待上架
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="product in displayedProducts"
                :key="product.id"
              >
                <!-- 商品图片与名称 -->
                <td>
                  <div class="product-name-cell">
                    <div class="product-thumbnail">
                      <!-- <img
                        v-if="
                          hasProductImage(product)
                        "
                        :src="
                          getProductImage(product)
                        "
                        :alt="
                          getProductName(product)
                        "
                        loading="lazy"
                        @error="
                          handleProductImageError(
                            product,
                          )
                        "
                      /> -->
                      <el-image
                        v-if="hasProductImage(product)"
                        class="product-preview-image"
                        :src="getProductImage(product)"
                        :preview-src-list="[
                          getProductImage(product),
                        ]"
                        :alt="getProductName(product)"
                        fit="contain"
                        loading="lazy"
                        preview-teleported
                        hide-on-click-modal
                        :infinite="false"
                        :z-index="10000"
                        @error="
                          handleProductImageError(product)
                        "
                      />

                      <i
                        v-else
                        class="bi bi-image"
                        aria-hidden="true"
                      ></i>
                    </div>

                    <div class="product-name">
                      <strong>
                        <AppCopyText
                          class="product-title-copy"
                          :value="getProductName(product)"
                          label="商品名"
                        />
                      </strong>

                      <span>
                        {{
                          product.english_name ||
                          '暂无英文名称'
                        }}
                      </span>
                    </div>
                  </div>
                </td>

                <!-- SKU -->
                <td class="sku-cell">
                  <AppCopyText
                    :value="product.customer_sku"
                    label="客户 SKU"
                  />
                </td>

                <td class="sku-cell">
                  <AppCopyText
                    :value="product.erp_sku"
                    label="ERP SKU"
                  />
                </td>

                <!-- 仓库与状态 -->
                <td>
                  {{ getWarehouseName(product) }}
                </td>

                <td>
                  <span class="status-tag">
                    {{ product.status_name || '—' }}
                  </span>
                </td>

                <td>
                  <span
                    class="inventory-status"
                    :class="{
                      missing:
                        product.inventory
                          ?.found === false,
                    }"
                  >
                    {{
                      getInventoryStateText(product)
                    }}
                  </span>
                </td>

                <!-- 库存数量 -->
                <td class="quantity-column">
                  {{
                    formatQuantity(
                      product.inventory?.total,
                    )
                  }}
                </td>

                <td class="quantity-column available">
                  {{
                    formatQuantity(
                      product.inventory?.available,
                    )
                  }}
                </td>

                <td class="quantity-column">
                  {{
                    formatQuantity(
                      product.inventory
                        ?.transferring,
                    )
                  }}
                </td>

                <td class="quantity-column">
                  {{
                    formatQuantity(
                      product.inventory
                        ?.waiting_for_shelf,
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
          class="card-view"
        >
          <article
            v-for="product in displayedProducts"
            :key="product.id"
            class="product-card"
          >
            <!-- 商品主图 -->
            <div class="card-image">
              <!-- <img
                v-if="hasProductImage(product)"
                :src="getProductImage(product)"
                :alt="getProductName(product)"
                loading="lazy"
                @error="
                  handleProductImageError(product)
                "
              /> -->
              <el-image
                v-if="hasProductImage(product)"
                class="product-preview-image"
                :src="getProductImage(product)"
                :preview-src-list="[
                  getProductImage(product),
                ]"
                :alt="getProductName(product)"
                fit="contain"
                loading="lazy"
                preview-teleported
                hide-on-click-modal
                :infinite="false"
                :z-index="10000"
                @error="
                  handleProductImageError(product)
                "
              />

              <div
                v-else
                class="image-placeholder"
              >
                <i
                  class="bi bi-image"
                  aria-hidden="true"
                ></i>

                <span>暂无商品图片</span>
              </div>
            </div>

            <!-- 商品基础信息 -->
            <div class="card-header">
              <div>
                <h4>
                  <AppCopyText
                    class="product-title-copy"
                    :value="getProductName(product)"
                    label="商品名"
                  />
                </h4>

                <p>
                  {{
                    product.english_name ||
                    '暂无英文名称'
                  }}
                </p>
              </div>

              <span class="status-tag">
                {{ product.status_name || '—' }}
              </span>
            </div>

            <!-- 商品资料 -->
            <dl class="card-info">
              <div>
                <dt>Customer SKU</dt>
                <dd>
                  <AppCopyText
                    :value="product.customer_sku"
                    label="客户 SKU"
                  />
                </dd>
              </div>

              <div>
                <dt>ERP SKU</dt>
                <dd>
                  <AppCopyText
                    :value="product.erp_sku"
                    label="ERP SKU"
                  />
                </dd>
              </div>

              <div class="full">
                <dt>主仓库</dt>
                <dd>
                  {{ getWarehouseName(product) }}
                </dd>
              </div>
            </dl>

            <!-- 库存信息 -->
            <div class="card-inventory">
              <header>
                <span>实时库存</span>

                <span
                  class="inventory-status"
                  :class="{
                    missing:
                      product.inventory
                        ?.found === false,
                  }"
                >
                  {{
                    getInventoryStateText(product)
                  }}
                </span>
              </header>

              <dl>
                <div>
                  <dt>总库存</dt>
                  <dd>
                    {{
                      formatQuantity(
                        product.inventory?.total,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>可用</dt>
                  <dd class="available">
                    {{
                      formatQuantity(
                        product.inventory?.available,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>在途</dt>
                  <dd>
                    {{
                      formatQuantity(
                        product.inventory
                          ?.transferring,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>待上架</dt>
                  <dd>
                    {{
                      formatQuantity(
                        product.inventory
                          ?.waiting_for_shelf,
                      )
                    }}
                  </dd>
                </div>
              </dl>
            </div>
          </article>
        </div>

        <!-- ==================== 分页 ==================== -->

        <footer class="pagination-bar">
          <AppSelect
            v-model="pageSize"
            :options="pageSizeOptions"
            :width="132"
            aria-label="每页商品数量"
            @change="changePageSize"
          />

          <div class="pagination-controls">
            <button
              type="button"
              :disabled="
                loading ||
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
                loading ||
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

<!-- ==================== 商品列表页面样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./product-list.scss"
></style>