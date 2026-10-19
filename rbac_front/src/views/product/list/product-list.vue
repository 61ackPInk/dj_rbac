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
                :class="{
                  'is-clickable':
                    canViewProductDetail,
                }"
                :tabindex="
                  canViewProductDetail
                    ? 0
                    : undefined
                "
                @click="
                  openProductDetail(product)
                "
                @keydown.enter="
                  openProductDetail(product)
                "
              >
                <!-- 商品图片与名称 -->
                <td>
                  <div class="product-name-cell">
                    <div class="product-thumbnail" @click.stop @keydown.stop>
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
                          @click.stop
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
                    @click.stop
                  />
                </td>

                <td class="sku-cell">
                  <AppCopyText
                    :value="product.erp_sku"
                    label="ERP SKU"
                    @click.stop
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
            :class="{
              'is-clickable':
                canViewProductDetail,
            }"
            :tabindex="
              canViewProductDetail
                ? 0
                : undefined
            "
            @click="
              openProductDetail(product)
            "
            @keydown.enter="
              openProductDetail(product)
            "
          >
            <!-- 商品主图 -->
            <div class="card-image" @click.stop @keydown.stop>
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
                    @click.stop
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
                    @click.stop
                  />
                </dd>
              </div>

              <div>
                <dt>ERP SKU</dt>
                <dd>
                  <AppCopyText
                    :value="product.erp_sku"
                    label="ERP SKU"
                    @click.stop
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

  <!-- ==================== 商品详情弹窗 ==================== -->

  <AppModal
    v-model="detailModalVisible"
    scope-class="product-detail-modal-scope"
    title="商品详情"
    :width="1000"
    :closable="!detailLoading"
    :close-on-overlay="!detailLoading"
    :close-on-escape="!detailLoading"
    @close="closeProductDetail"
  >
    <!-- ==================== 详情加载状态 ==================== -->

    <div
      v-if="detailLoading"
      class="product-detail-loading"
    >
      <i
        class="bi bi-arrow-clockwise"
        aria-hidden="true"
      ></i>

      <span>正在加载商品详情...</span>
    </div>

    <!-- ==================== 商品详情内容 ==================== -->

    <div
      v-else-if="selectedProduct"
      class="product-detail"
    >
      <!-- ==================== 商品头部 ==================== -->

      <header class="detail-heading">
        <div class="detail-main-image">
          <el-image
            v-if="detailImages.length"
            :src="detailImages[0]"
            :preview-src-list="detailImages"
            :alt="getProductName(selectedProduct)"
            fit="contain"
            preview-teleported
            hide-on-click-modal
            :z-index="10000"
          >
            <template #error>
              <div class="detail-image-empty">
                <i
                  class="bi bi-image"
                  aria-hidden="true"
                ></i>
              </div>
            </template>
          </el-image>

          <div
            v-else
            class="detail-image-empty"
          >
            <i
              class="bi bi-image"
              aria-hidden="true"
            ></i>
          </div>
        </div>

        <div class="detail-heading-content">
          <div class="detail-title-row">
            <div>
              <h2>
                {{
                  getProductName(
                    selectedProduct,
                  )
                }}
              </h2>

              <p>
                {{
                  selectedProduct.english_name ||
                  '暂无英文名称'
                }}
              </p>
            </div>

            <span class="status-tag">
              {{
                selectedProduct.status_name ||
                '—'
              }}
            </span>
          </div>

          <dl class="detail-summary">
            <div>
              <dt>客户 SKU</dt>
              <dd>
                <AppCopyText
                  :value="
                    selectedProduct.customer_sku
                  "
                  label="客户 SKU"
                />
              </dd>
            </div>

            <div>
              <dt>ERP SKU</dt>
              <dd>
                <AppCopyText
                  :value="
                    selectedProduct.erp_sku
                  "
                  label="ERP SKU"
                />
              </dd>
            </div>

            <div>
              <dt>参考编码</dt>
              <dd>
                {{
                  formatDetailValue(
                    selectedProduct.reference_code,
                  )
                }}
              </dd>
            </div>

            <div>
              <dt>元仓分类 ID</dt>
              <dd>
                {{
                  formatDetailValue(
                    selectedProduct.category_id,
                  )
                }}
              </dd>
            </div>

            <div>
              <dt>商品类型</dt>
              <dd>
                {{
                  formatDetailValue(
                    selectedProduct
                      .product_type_name,
                  )
                }}
              </dd>
            </div>

            <div>
              <dt>成交单位</dt>
              <dd>
                {{
                  selectedProduct.unit_name ||
                  selectedProduct.unit_code ||
                  '—'
                }}
              </dd>
            </div>
          </dl>
        </div>
      </header>

      <!-- ==================== 商品图片 ==================== -->

      <section
        v-if="detailImages.length > 1"
        class="detail-section"
      >
        <h3>商品图片</h3>

        <div class="detail-image-list">
          <el-image
            v-for="(image, index) in detailImages"
            :key="`${image}-${index}`"
            :src="image"
            :preview-src-list="detailImages"
            :initial-index="index"
            :alt="
              `${getProductName(selectedProduct)} ${
                index + 1
              }`
            "
            fit="contain"
            loading="lazy"
            preview-teleported
            hide-on-click-modal
            :z-index="10000"
          >
            <template #error>
              <div class="detail-image-empty">
                <i
                  class="bi bi-image"
                  aria-hidden="true"
                ></i>
              </div>
            </template>
          </el-image>
        </div>
      </section>

      <!-- ==================== 实时库存 ==================== -->

      <section class="detail-section">
        <h3>实时库存</h3>

        <div
          v-if="
            selectedProduct.inventory
              ?.found === false
          "
          class="inventory-missing-notice"
        >
          <i
            class="bi bi-exclamation-circle"
            aria-hidden="true"
          ></i>

          没有匹配到该商品的库存记录
        </div>

        <dl class="inventory-grid">
          <div>
            <dt>仓库编码</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.inventory
                    ?.warehouse_code,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>站点编码</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.inventory
                    ?.site_code,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>备货中</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
                    ?.preparing,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>在途</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
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
                  selectedProduct.inventory
                    ?.waiting_for_shelf,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>总库存</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
                    ?.total,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>占用库存</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
                    ?.occupied,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>未发货</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
                    ?.unshipped,
                )
              }}
            </dd>
          </div>

          <div class="available">
            <dt>可用库存</dt>
            <dd>
              {{
                formatQuantity(
                  selectedProduct.inventory
                    ?.available,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>库存状态</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.inventory
                    ?.status_name,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>锁定状态</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.inventory
                    ?.lock_status_name,
                )
              }}
            </dd>
          </div>
        </dl>
      </section>

      <!-- ==================== 申报与商品资料 ==================== -->

      <section class="detail-section">
        <h3>商品资料</h3>

        <dl class="detail-grid">
          <div>
            <dt>申报中文名</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct
                    .declared_chinese_name,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>申报英文名</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.declared_name,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>商品属性</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct
                    .product_attribute_name,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>是否有品牌</dt>
            <dd>
              {{
                formatBoolean(
                  selectedProduct.has_brand,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>品牌名称</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.brand_name,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>型号</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.model,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>用途</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.usage,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>材质</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.material,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>参考成本价</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct
                    .reference_cost_price,
                )
              }}
            </dd>
          </div>

          <div class="full">
            <dt>商品链接</dt>
            <dd>
              <a
                v-if="selectedProduct.product_link"
                :href="
                  selectedProduct.product_link
                "
                target="_blank"
                rel="noopener noreferrer"
              >
                {{
                  selectedProduct.product_link
                }}
              </a>

              <span v-else>—</span>
            </dd>
          </div>
        </dl>
      </section>

      <!-- ==================== 商品规格 ==================== -->

      <section class="detail-section">
        <h3>商品规格</h3>

        <dl class="specification-grid">
          <div>
            <dt>商品长度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.length,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>商品宽度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.width,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>商品高度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.height,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>商品重量</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.weight,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>包装长度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.package_length,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>包装宽度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.package_width,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>包装高度</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.package_height,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>包装重量</dt>
            <dd>
              {{
                formatDetailValue(
                  selectedProduct.specifications
                    ?.package_weight,
                )
              }}
            </dd>
          </div>
        </dl>
      </section>

      <!-- ==================== 关联仓库 ==================== -->

      <section class="detail-section">
        <h3>关联仓库</h3>

        <div
          v-if="
            selectedProduct.warehouses?.length
          "
          class="detail-table-scroll"
        >
          <table class="detail-table">
            <thead>
              <tr>
                <th>仓库编码</th>
                <th>仓库名称</th>
                <th>采购价</th>
                <th>库存价</th>
                <th>更新时间</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="(
                  warehouse,
                  index
                ) in selectedProduct.warehouses"
                :key="
                  warehouse.code ||
                  index
                "
              >
                <td data-label="仓库编码">
                  {{
                    formatDetailValue(
                      warehouse.code,
                    )
                  }}
                </td>

                <td data-label="仓库名称">
                  {{
                    formatDetailValue(
                      warehouse.name,
                    )
                  }}
                </td>

                <td data-label="采购价">
                  {{
                    formatDetailValue(
                      warehouse.purchase_price,
                    )
                  }}
                </td>

                <td data-label="库存价">
                  {{
                    formatDetailValue(
                      warehouse.stock_price,
                    )
                  }}
                </td>

                <td data-label="更新时间">
                  {{
                    formatDateTime(
                      warehouse.updated_at,
                    )
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p
          v-else
          class="detail-empty"
        >
          暂无关联仓库信息
        </p>
      </section>

      <!-- ==================== 海关申报 ==================== -->

      <section class="detail-section">
        <h3>海关申报</h3>

        <div class="customs-grid">
          <div class="customs-card">
            <h4>出境申报</h4>

            <dl>
              <div>
                <dt>国家或地区</dt>
                <dd>
                  {{
                    formatDetailValue(
                      selectedProduct
                        .outbound_customs
                        ?.country,
                    )
                  }}
                </dd>
              </div>

              <div>
                <dt>申报价</dt>
                <dd>
                  {{
                    formatDetailValue(
                      selectedProduct
                        .outbound_customs
                        ?.price,
                    )
                  }}
                </dd>
              </div>
            </dl>
          </div>

          <div class="customs-card">
            <h4>入境申报</h4>

            <div
              v-if="
                selectedProduct
                  .inbound_customs?.length
              "
              class="customs-list"
            >
              <dl
                v-for="(
                  customs,
                  index
                ) in selectedProduct
                  .inbound_customs"
                :key="index"
              >
                <div>
                  <dt>国家或地区</dt>
                  <dd>
                    {{
                      formatDetailValue(
                        customs.country,
                      )
                    }}
                  </dd>
                </div>

                <div>
                  <dt>申报价</dt>
                  <dd>
                    {{
                      formatDetailValue(
                        customs.price,
                      )
                    }}
                  </dd>
                </div>
              </dl>
            </div>

            <p
              v-else
              class="detail-empty"
            >
              暂无入境申报信息
            </p>
          </div>
        </div>
      </section>

      <!-- ==================== 时间信息 ==================== -->

      <section class="detail-section">
        <h3>时间信息</h3>

        <dl class="detail-grid">
          <div>
            <dt>创建时间</dt>
            <dd>
              {{
                formatDateTime(
                  selectedProduct.created_at,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>更新时间</dt>
            <dd>
              {{
                formatDateTime(
                  selectedProduct.updated_at,
                )
              }}
            </dd>
          </div>
        </dl>
      </section>
    </div>

    <!-- ==================== 弹窗底部 ==================== -->

    <template #footer>
      <button
        class="detail-close-button"
        type="button"
        :disabled="detailLoading"
        @click="closeProductDetail"
      >
        关闭
      </button>
    </template>
  </AppModal>

</template>

<!-- ==================== 商品列表页面样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./product-list.scss"
></style>

<!-- ==================== 商品详情弹窗样式 ==================== -->

<!--
  AppModal 通过 Teleport 渲染到 body，
  因此弹窗业务样式不能使用 scoped。
-->
<style
  lang="scss"
  src="./product-list-modal.scss"
></style>