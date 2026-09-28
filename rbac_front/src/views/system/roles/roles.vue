<!-- ==================== 角色管理业务逻辑 ==================== -->

<script src="./roles.js"></script>

<template>
  <div class="roles-page">
    <!-- ==================== 页面标题 ==================== -->

    <header class="page-heading">
      <div>
        <h1>角色管理</h1>

        <p>
          管理系统角色、角色权重和启用状态。
        </p>
      </div>

      <!-- 只有根管理员可以创建角色 -->
      <button
        v-if="canManageRoles"
        class="primary-button"
        type="button"
        @click="openCreateModal"
      >
        <i
          class="bi bi-plus-lg"
          aria-hidden="true"
        ></i>

        <span>创建角色</span>
      </button>
    </header>

    <!-- ==================== 角色管理面板 ==================== -->

    <section class="role-panel">
      <!-- ==================== 搜索与筛选 ==================== -->

      <div class="toolbar">
        <div class="toolbar-left">
          <!-- 搜索角色 -->
          <label class="search-box">
            <i
              class="bi bi-search"
              aria-hidden="true"
            ></i>

            <input
              v-model="keyword"
              type="search"
              placeholder="搜索角色名称、编码或描述"
              aria-label="搜索角色"
            />
          </label>

          <!-- 状态筛选 -->
          <AppSelect
            v-model="statusFilter"
            class="toolbar-select"
            :options="statusFilterOptions"
            :width="132"
            placeholder="全部状态"
            aria-label="按状态筛选"
          />
        </div>

        <div class="toolbar-right">
          <!-- 刷新角色列表 -->
          <button
            class="refresh-button"
            type="button"
            :disabled="loading"
            aria-label="刷新角色列表"
            title="刷新角色列表"
            @click="loadRoles"
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
            aria-label="角色显示方式"
          >
            <button
              class="view-button"
              :class="{
                'is-active':
                  viewMode === 'list',
              }"
              type="button"
              aria-label="列表显示"
              :aria-pressed="
                viewMode === 'list'
              "
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
                'is-active':
                  viewMode === 'card',
              }"
              type="button"
              aria-label="卡片显示"
              :aria-pressed="
                viewMode === 'card'
              "
              @click="setViewMode('card')"
            >
              <i
                class="bi bi-grid"
                aria-hidden="true"
              ></i>
            </button>
          </div>
        </div>
      </div>

      <!-- ==================== 结果统计 ==================== -->

      <div class="result-summary">
        <span>
          共找到
          <strong>
            {{ filteredRoles.length }}
          </strong>
          个角色
        </span>

        <span class="summary-status">
          已启用 {{ activeCount }} 个，
          已停用 {{ disabledCount }} 个
        </span>
      </div>

      <!-- ==================== 加载状态 ==================== -->

      <div
        v-if="loading && roles.length === 0"
        class="page-state"
      >
        <i
          class="
            bi bi-arrow-clockwise
            state-loading
          "
          aria-hidden="true"
        ></i>

        <strong>正在加载角色</strong>
        <span>请稍候...</span>
      </div>

      <!-- ==================== 错误状态 ==================== -->

      <div
        v-else-if="errorMessage"
        class="page-state error"
        role="alert"
      >
        <i
          class="bi bi-exclamation-circle"
          aria-hidden="true"
        ></i>

        <strong>角色数据加载失败</strong>
        <span>{{ errorMessage }}</span>

        <button
          class="secondary-button"
          type="button"
          @click="loadRoles"
        >
          重新加载
        </button>
      </div>

      <!-- ==================== 空状态 ==================== -->

      <div
        v-else-if="
          filteredRoles.length === 0
        "
        class="page-state"
      >
        <i
          class="bi bi-person-badge"
          aria-hidden="true"
        ></i>

        <strong>没有找到角色</strong>

        <span>
          请尝试修改搜索内容或筛选条件。
        </span>
      </div>

      <!-- ==================== 列表显示模式 ==================== -->

      <div
        v-else-if="viewMode === 'list'"
        class="list-view"
      >
        <table class="role-table">
          <thead>
            <tr>
              <th>角色</th>
              <th>角色编码</th>
              <th>权重</th>
              <th>角色描述</th>
              <th>状态</th>
              <th>更新时间</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="role in filteredRoles"
              :key="role.id"
            >
              <!-- 角色基本信息 -->
              <td>
                <div class="role-cell">
                  <span class="role-avatar">
                    {{ getRoleInitial(role) }}
                  </span>

                  <div class="role-basic">
                    <strong>
                      {{ role.name }}
                    </strong>

                    <span>
                      ID: {{ role.id }}
                    </span>
                  </div>
                </div>
              </td>

              <!-- 角色编码 -->
              <td>
                <code class="code-tag">
                  {{ role.code }}
                </code>
              </td>

              <!-- 角色权重 -->
              <td>
                <span class="rank-value">
                  {{ role.rank }}
                </span>
              </td>

              <!-- 角色描述 -->
              <td>
                <span class="description-text">
                  {{
                    role.description ||
                    '暂无描述'
                  }}
                </span>
              </td>

              <!-- 角色状态 -->
              <td>
                <span
                  class="status-tag"
                  :class="
                    role.is_active
                      ? 'enabled'
                      : 'disabled'
                  "
                >
                  {{
                    role.is_active
                      ? '已启用'
                      : '已停用'
                  }}
                </span>
              </td>

              <!-- 更新时间 -->
              <td>
                {{ formatTime(role.update_time) }}
              </td>

              <!-- 角色操作 -->
              <td>
                <div class="action-group">
                  <button
                    class="table-action"
                    type="button"
                    @click="
                      openDetailModal(role)
                    "
                  >
                    查看
                  </button>

                  <button
                    v-if="canManageRoles"
                    class="table-action"
                    type="button"
                    @click="
                      openEditModal(role)
                    "
                  >
                    编辑
                  </button>

                  <button
                    v-if="canManageRoles"
                    class="table-action"
                    :class="
                      role.is_active
                        ? 'disable'
                        : 'enable'
                    "
                    type="button"
                    @click="
                      openStatusModal(role)
                    "
                  >
                    {{
                      role.is_active
                        ? '停用'
                        : '启用'
                    }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ==================== 卡片显示模式 ==================== -->

      <div
        v-else
        class="card-view"
      >
        <article
          v-for="role in filteredRoles"
          :key="role.id"
          class="role-card"
        >
          <!-- 卡片头部 -->
          <header class="role-card-header">
            <div class="role-card-person">
              <span class="card-avatar">
                {{ getRoleInitial(role) }}
              </span>

              <div class="card-role-info">
                <strong>{{ role.name }}</strong>
                <span>{{ role.code }}</span>
              </div>
            </div>

            <span
              class="status-tag"
              :class="
                role.is_active
                  ? 'enabled'
                  : 'disabled'
              "
            >
              {{
                role.is_active
                  ? '已启用'
                  : '已停用'
              }}
            </span>
          </header>

          <!-- 卡片资料 -->
          <dl class="role-card-body">
            <div class="card-info-row">
              <dt>角色权重</dt>
              <dd>
                <span class="rank-value">
                  {{ role.rank }}
                </span>
              </dd>
            </div>

            <div class="card-info-row">
              <dt>角色编码</dt>
              <dd>{{ role.code }}</dd>
            </div>

            <div class="card-info-row">
              <dt>角色描述</dt>

              <dd
                class="card-description"
                :title="
                  role.description ||
                  '暂无描述'
                "
              >
                {{
                  role.description ||
                  '暂无描述'
                }}
              </dd>
            </div>

            <div class="card-info-row">
              <dt>更新时间</dt>
              <dd>
                {{
                  formatTime(
                    role.update_time,
                  )
                }}
              </dd>
            </div>
          </dl>

          <!-- 卡片操作 -->
          <footer class="role-card-footer">
            <button
              class="card-action"
              type="button"
              @click="
                openDetailModal(role)
              "
            >
              查看
            </button>

            <button
              v-if="canManageRoles"
              class="card-action"
              type="button"
              @click="openEditModal(role)"
            >
              编辑
            </button>

            <button
              v-if="canManageRoles"
              class="card-action"
              :class="{
                disable: role.is_active,
                enable: !role.is_active,
              }"
              type="button"
              @click="
                openStatusModal(role)
              "
            >
              {{
                role.is_active
                  ? '停用'
                  : '启用'
              }}
            </button>
          </footer>
        </article>
      </div>
    </section>

    <!-- ==================== 创建与编辑角色弹出层 ==================== -->

    <AppModal
      v-model="formModalVisible"
      :title="formModalTitle"
      :width="640"
      :closable="!submitting"
      :close-on-overlay="!submitting"
      :close-on-escape="!submitting"
    >
      <form
        id="role-form"
        class="role-form"
        novalidate
        @submit.prevent="submitRoleForm"
      >
        <div class="form-grid">
          <!-- 角色名称 -->
          <label class="form-field">
            <span class="field-label">
              角色名称
              <i aria-hidden="true">*</i>
            </span>

            <input
              v-model="roleForm.name"
              type="text"
              maxlength="50"
              autocomplete="off"
              placeholder="例如：系统管理员"
            />
          </label>

          <!-- 角色编码 -->
          <label class="form-field">
            <span class="field-label">
              角色编码
              <i aria-hidden="true">*</i>
            </span>

            <input
              v-model="roleForm.code"
              type="text"
              maxlength="50"
              autocomplete="off"
              placeholder="例如：SYSTEM_ADMIN"
              @blur="normalizeRoleCode"
            />

            <small class="field-help">
              以字母开头，只能使用字母、数字和下划线。
            </small>
          </label>

          <!-- 角色权重 -->
          <label class="form-field">
            <span class="field-label">
              角色权重
              <i aria-hidden="true">*</i>
            </span>

            <input
              v-model.number="roleForm.rank"
              type="number"
              min="1"
              step="1"
              inputmode="numeric"
              placeholder="请输入大于0的整数"
            />

            <small class="field-help">
              数字越大，角色等级越高。
            </small>
          </label>

          <!-- 角色状态 -->
          <label class="form-field">
            <span class="field-label">
              角色状态
            </span>

            <AppSelect
              v-model="roleForm.isActive"
              :options="roleStatusOptions"
              placeholder="请选择角色状态"
            />
          </label>

          <!-- 角色描述 -->
          <label class="form-field full">
            <span class="field-label">
              角色描述
            </span>

            <textarea
              v-model="
                roleForm.description
              "
              maxlength="255"
              rows="4"
              placeholder="请输入角色用途说明"
            ></textarea>

            <small class="field-count">
              {{
                roleForm.description.length
              }}/255
            </small>
          </label>
        </div>
      </form>

      <template #footer>
        <button
          class="secondary-button"
          type="button"
          :disabled="submitting"
          @click="closeFormModal"
        >
          取消
        </button>

        <button
          class="primary-button"
          type="submit"
          form="role-form"
          :disabled="submitting"
        >
          <i
            v-if="submitting"
            class="
              bi bi-arrow-clockwise
              button-loading
            "
            aria-hidden="true"
          ></i>

          {{
            submitting
              ? '正在保存...'
              : isCreateMode
                ? '创建角色'
                : '保存修改'
          }}
        </button>
      </template>
    </AppModal>

    <!-- ==================== 角色详情弹出层 ==================== -->

    <AppModal
      v-model="detailModalVisible"
      title="角色信息"
      :width="620"
      :closable="!detailLoading"
      :close-on-overlay="
        !detailLoading
      "
      :close-on-escape="
        !detailLoading
      "
    >
      <!-- 详情加载状态 -->
      <div
        v-if="detailLoading"
        class="detail-loading"
      >
        <i
          class="bi bi-arrow-clockwise"
          aria-hidden="true"
        ></i>

        <span>正在加载角色信息...</span>
      </div>

      <!-- 角色详情 -->
      <div
        v-else-if="selectedRole"
        class="role-detail"
      >
        <header class="detail-profile">
          <span class="detail-avatar">
            {{ getRoleInitial(selectedRole) }}
          </span>

          <div>
            <h3>{{ selectedRole.name }}</h3>
            <p>{{ selectedRole.code }}</p>
          </div>

          <span
            class="status-tag"
            :class="
              selectedRole.is_active
                ? 'enabled'
                : 'disabled'
            "
          >
            {{
              selectedRole.is_active
                ? '已启用'
                : '已停用'
            }}
          </span>
        </header>

        <dl class="detail-grid">
          <div>
            <dt>角色名称</dt>
            <dd>{{ selectedRole.name }}</dd>
          </div>

          <div>
            <dt>角色编码</dt>
            <dd>{{ selectedRole.code }}</dd>
          </div>

          <div>
            <dt>角色权重</dt>
            <dd>{{ selectedRole.rank }}</dd>
          </div>

          <div>
            <dt>角色状态</dt>
            <dd>
              {{
                selectedRole.is_active
                  ? '已启用'
                  : '已停用'
              }}
            </dd>
          </div>

          <div class="full">
            <dt>角色描述</dt>
            <dd>
              {{
                selectedRole.description ||
                '暂无描述'
              }}
            </dd>
          </div>

          <div>
            <dt>创建时间</dt>
            <dd>
              {{
                formatTime(
                  selectedRole.create_time,
                )
              }}
            </dd>
          </div>

          <div>
            <dt>更新时间</dt>
            <dd>
              {{
                formatTime(
                  selectedRole.update_time,
                )
              }}
            </dd>
          </div>
        </dl>
      </div>

      <template #footer>
        <button
          class="secondary-button"
          type="button"
          :disabled="detailLoading"
          @click="closeDetailModal"
        >
          关闭
        </button>

        <button
          v-if="canManageRoles"
          class="primary-button"
          type="button"
          :disabled="
            detailLoading ||
            !selectedRole
          "
          @click="editSelectedRole"
        >
          <i
            class="bi bi-pencil"
            aria-hidden="true"
          ></i>

          编辑角色
        </button>
      </template>
    </AppModal>

    <!-- ==================== 状态确认弹出层 ==================== -->

    <AppModal
      v-model="statusModalVisible"
      :title="statusModalTitle"
      :width="430"
      :closable="!submitting"
      :close-on-overlay="!submitting"
      :close-on-escape="!submitting"
    >
      <div
        v-if="statusTargetRole"
        class="status-confirm"
      >
        <div
          class="confirm-icon"
          :class="{
            enable:
              !statusTargetRole.is_active,
          }"
          aria-hidden="true"
        >
          <i
            class="bi"
            :class="
              statusTargetRole.is_active
                ? 'bi-person-x'
                : 'bi-person-check'
            "
          ></i>
        </div>

        <div>
          <h3>
            {{
              statusTargetRole.is_active
                ? `确定停用“${statusTargetRole.name}”吗？`
                : `确定启用“${statusTargetRole.name}”吗？`
            }}
          </h3>

          <p>
            {{
              statusTargetRole.is_active
                ? '停用后，该角色不能再分配给用户，已有角色数据会继续保留。'
                : '启用后，该角色可以重新分配给用户。'
            }}
          </p>
        </div>
      </div>

      <template #footer>
        <button
          class="secondary-button"
          type="button"
          :disabled="submitting"
          @click="closeStatusModal"
        >
          取消
        </button>

        <button
          class="confirm-button"
          :class="{
            danger:
              statusTargetRole?.is_active,
            success:
              !statusTargetRole?.is_active,
          }"
          type="button"
          :disabled="submitting"
          @click="confirmRoleStatus"
        >
          {{
            submitting
              ? '正在处理...'
              : statusActionText
          }}
        </button>
      </template>
    </AppModal>
  </div>
</template>

<!-- ==================== 角色管理页面样式 ==================== -->

<style
  scoped
  lang="scss"
  src="./roles.scss"
></style>

<!-- ==================== 角色弹出层业务样式 ==================== -->

<style
  lang="scss"
  src="./roles-modal.scss"
></style>