<!-- ==================== 用户管理业务逻辑 ==================== -->
<script src="./users.js"></script>

<template>
  <div class="users-page">
    <!-- ==================== 页面标题 ==================== -->
    <header class="page-heading">
      <div>
        <h1>用户管理</h1>
        <p>管理系统用户、角色和账号状态。</p>
      </div>

      <button v-if="canCreateUser" class="primary-button" type="button" @click="openCreateModal">
        <i class="bi bi-plus-lg" aria-hidden="true"></i>

        <span>创建用户</span>
      </button>
    </header>

    <!-- ==================== 用户管理面板 ==================== -->
    <section class="user-panel">
      <!-- ==================== 搜索与筛选 ==================== -->
      <div class="toolbar">
        <div class="toolbar-left">
          <!-- 搜索用户 -->
          <label class="search-box">
            <i class="bi bi-search" aria-hidden="true"></i>

            <input v-model="keyword" type="search" placeholder="搜索用户名、邮箱或角色" aria-label="搜索用户" />
          </label>

          <!-- 角色筛选 -->
          <AppSelect v-model="roleFilter" class="toolbar-select" :options="roleFilterOptions" :width="132"
            placeholder="全部角色" aria-label="按角色筛选" />

          <!-- 状态筛选 -->
          <AppSelect v-model="statusFilter" class="toolbar-select" :options="statusFilterOptions" :width="132"
            placeholder="全部状态" aria-label="按状态筛选" />
        </div>

        <div class="toolbar-right">
          <!-- 刷新用户列表 -->
          <button class="refresh-button" type="button" :disabled="loading" aria-label="刷新用户列表" title="刷新用户列表"
            @click="loadPageData">
            <i class="bi bi-arrow-clockwise" :class="{ 'is-rotating': loading }" aria-hidden="true"></i>
          </button>

          <!-- 显示模式切换 -->
          <div class="view-switch" role="group" aria-label="用户显示方式">
            <button class="view-button" :class="{
              'is-active': viewMode === 'list',
            }" type="button" aria-label="列表显示" :aria-pressed="viewMode === 'list'" @click="setViewMode('list')">
              <i class="bi bi-list-ul" aria-hidden="true"></i>
            </button>

            <button class="view-button" :class="{
              'is-active': viewMode === 'card',
            }" type="button" aria-label="卡片显示" :aria-pressed="viewMode === 'card'" @click="setViewMode('card')">
              <i class="bi bi-grid" aria-hidden="true"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- ==================== 结果统计 ==================== -->
      <div class="result-summary">
        <span>
          共找到
          <strong>{{ filteredUsers.length }}</strong>
          位用户
        </span>

        <span class="summary-status">
          已启用 {{ activeCount }} 位，
          已禁用 {{ disabledCount }} 位
        </span>
      </div>

      <!-- ==================== 加载状态 ==================== -->
      <div v-if="loading && users.length === 0" class="page-state">
        <i class="bi bi-arrow-clockwise state-loading" aria-hidden="true"></i>

        <strong>正在加载用户</strong>
        <span>请稍候...</span>
      </div>

      <!-- ==================== 错误状态 ==================== -->
      <div v-else-if="errorMessage" class="page-state error" role="alert">
        <i class="bi bi-exclamation-circle" aria-hidden="true"></i>

        <strong>用户数据加载失败</strong>
        <span>{{ errorMessage }}</span>

        <button class="secondary-button" type="button" @click="loadPageData">
          重新加载
        </button>
      </div>

      <!-- ==================== 空状态 ==================== -->
      <div v-else-if="filteredUsers.length === 0" class="page-state">
        <i class="bi bi-person-x" aria-hidden="true"></i>

        <strong>没有找到用户</strong>
        <span>请尝试修改搜索内容或筛选条件。</span>
      </div>

      <!-- ==================== 列表显示模式 ==================== -->
      <div v-else-if="viewMode === 'list'" class="list-view">
        <table class="user-table">
          <thead>
            <tr>
              <th>用户</th>
              <th>用户名</th>
              <th>角色</th>
              <th>最后登录</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <!-- 用户信息 -->
              <td>
                <div class="user-cell">
                  <span class="user-avatar">
                    {{ getUserInitial(user) }}
                  </span>

                  <div class="user-basic">
                    <strong>{{ user.username }}</strong>
                    <span>
                      {{ user.email || '未填写邮箱' }}
                    </span>
                  </div>
                </div>
              </td>

              <!-- 用户名 -->
              <td>{{ user.username }}</td>

              <!-- 角色 -->
              <td>
                <span v-if="user.role" class="role-tag">
                  {{ getUserRoleName(user) }}
                </span>

                <span v-else class="role-tag empty">
                  未分配角色
                </span>
              </td>

              <!-- 最后登录 -->
              <td>
                {{ formatTime(user.last_login) }}
              </td>

              <!-- 用户状态 -->
              <td>
                <span class="status-tag" :class="user.is_active
                  ? 'enabled'
                  : 'disabled'
                  ">
                  {{
                    user.is_active
                      ? '已启用'
                      : '已禁用'
                  }}
                </span>
              </td>

              <!-- 用户操作 -->
              <td>
                <div class="action-group">
                  <!-- 列表-查看 -->
                  <button v-if="canViewUserDetail" class="table-action" type="button" @click="openDetailModal(user)">
                    查看
                  </button>
                  <!-- 列表-编辑 -->
                  <button v-if="canEditUser" class="table-action" type="button" @click="openEditModal(user)">
                    编辑
                  </button>
                  <!-- 列表-重置密码 -->
                  <button v-if="canResetUserPassword && !user.is_root" class="table-action" type="button"
                    @click="openPasswordModal(user)">
                    重置密码
                  </button>
                  <!-- 列表-状态 -->
                  <button v-if="canChangeUserStatus" class="table-action" :class="user.is_active ? 'disable' : 'enable'"
                    type="button" @click="openStatusModal(user)">
                    {{ user.is_active ? '禁用' : '启用' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ==================== 卡片显示模式 ==================== -->
      <div v-else class="card-view">
        <article v-for="user in filteredUsers" :key="user.id" class="user-card">
          <!-- 用户卡片头部 -->
          <header class="user-card-header">
            <div class="user-card-person">
              <span class="card-avatar">
                {{ getUserInitial(user) }}
              </span>

              <div class="card-user-info">
                <strong>{{ user.username }}</strong>
                <span>@{{ user.username }}</span>
              </div>
            </div>

            <span class="status-tag" :class="user.is_active
              ? 'enabled'
              : 'disabled'
              ">
              {{
                user.is_active
                  ? '已启用'
                  : '已禁用'
              }}
            </span>
          </header>

          <!-- 用户卡片信息 -->
          <dl class="user-card-body">
            <div class="card-info-row">
              <dt>角色</dt>
              <dd>{{ getUserRoleName(user) }}</dd>
            </div>

            <div class="card-info-row">
              <dt>电子邮箱</dt>
              <dd>{{ user.email || '—' }}</dd>
            </div>

            <div class="card-info-row">
              <dt>创建时间</dt>
              <dd>
                {{ formatTime(user.create_time) }}
              </dd>
            </div>

            <div class="card-info-row">
              <dt>最后登录</dt>
              <dd>
                {{ formatTime(user.last_login) }}
              </dd>
            </div>
          </dl>

          <!-- 用户卡片操作 -->
          <footer class="user-card-footer">
            <!-- 卡片-查看 -->
            <button v-if="canViewUserDetail" class="card-action" type="button" @click="openDetailModal(user)">
              查看
            </button>
            <!-- 卡片-编辑 -->
            <button v-if="canEditUser" class="card-action" type="button" @click="openEditModal(user)">
              编辑
            </button>
            <!-- 卡片-重置密码 -->
            <button v-if="canResetUserPassword && !user.is_root" class="card-action" type="button"
              @click="openPasswordModal(user)">
              重置密码
            </button>
            <!-- 卡片-状态 -->
            <button v-if="canChangeUserStatus" class="card-action"
              :class="{ disable: user.is_active, enable: !user.is_active, }" type="button"
              @click="openStatusModal(user)">
              {{ user.is_active ? '禁用' : '启用' }}
            </button>
          </footer>
        </article>
      </div>
    </section>

    <!-- ==================== 创建与编辑用户弹出层 ==================== -->
    <AppModal v-model="formModalVisible" scope-class="users-modal-scope" :title="formModalTitle" :width="620"
      :closable="!submitting" :close-on-overlay="!submitting" :close-on-escape="!submitting">
      <form id="user-form" class="user-form" novalidate @submit.prevent="submitUserForm">
        <div class="form-grid">
          <!-- 用户名 -->
          <label v-if="isCreateMode || canUpdateUser" class="form-field full">
            <span class="field-label">
              用户名
              <i aria-hidden="true">*</i>
            </span>

            <input v-model="userForm.username" type="text" maxlength="20" autocomplete="off"
              placeholder="请输入 4～20 位用户名" />
          </label>

          <!-- 邮箱 -->
          <label v-if="isCreateMode || canUpdateUser" class="form-field full">
            <span class="field-label">
              电子邮箱
            </span>

            <input v-model="userForm.email" type="email" autocomplete="off" placeholder="请输入电子邮箱" />
          </label>

          <!-- 创建时输入密码 -->
          <template v-if="isCreateMode">
            <label class="form-field">
              <span class="field-label">
                密码
                <i aria-hidden="true">*</i>
              </span>

              <input v-model="userForm.password" type="password" autocomplete="new-password" placeholder="请输入密码" />
            </label>

            <label class="form-field">
              <span class="field-label">
                确认密码
                <i aria-hidden="true">*</i>
              </span>

              <input v-model="userForm.passwordConfirm" type="password" autocomplete="new-password"
                placeholder="请再次输入密码" />
            </label>
          </template>

          <!-- 用户角色 -->
          <!-- 拥有分配角色权限时显示 -->
          <label v-if="canAssignUserRole" class="form-field">
            <span class="field-label">
              用户角色
            </span>

            <AppSelect v-model="userForm.roleId" :options="userRoleOptions" placeholder="请选择用户角色" />
          </label>

          <!-- 用户状态 -->
          <!--
            创建用户时可以设置初始状态。

            编辑已有用户时，
            状态通过独立的启用/禁用按钮修改。
          -->
          <label v-if="isCreateMode && canChangeUserStatus" class="form-field">
            <span class="field-label">
              账号状态
            </span>

            <AppSelect v-model="userForm.isActive" :options="userStatusOptions" placeholder="请选择账号状态" />
          </label>
        </div>
      </form>

      <template #footer>
        <button class="secondary-button" type="button" :disabled="submitting" @click="closeFormModal">
          取消
        </button>

        <button class="primary-button" type="submit" form="user-form" :disabled="submitting">
          <i v-if="submitting" class="bi bi-arrow-clockwise button-loading" aria-hidden="true"></i>

          {{
            submitting
              ? '正在保存...'
              : isCreateMode
                ? '创建用户'
                : '保存修改'
          }}
        </button>
      </template>
    </AppModal>

    <!-- ==================== 用户详情弹出层 ==================== -->
    <AppModal v-model="detailModalVisible" scope-class="users-modal-scope" title="用户信息" :width="620"
      :closable="!detailLoading" :close-on-overlay="!detailLoading" :close-on-escape="!detailLoading">
      <!-- 详情加载状态 -->
      <div v-if="detailLoading" class="detail-loading">
        <i class="bi bi-arrow-clockwise" aria-hidden="true"></i>

        <span>正在加载用户信息...</span>
      </div>

      <!-- 用户详情 -->
      <div v-else-if="selectedUser" class="user-detail">
        <!-- 详情头部 -->
        <header class="detail-profile">
          <span class="detail-avatar">
            {{ getUserInitial(selectedUser) }}
          </span>

          <div>
            <h3>{{ selectedUser.username }}</h3>
            <p>@{{ selectedUser.username }}</p>
          </div>

          <span class="status-tag" :class="selectedUser.is_active
            ? 'enabled'
            : 'disabled'
            ">
            {{
              selectedUser.is_active
                ? '已启用'
                : '已禁用'
            }}
          </span>
        </header>

        <!-- 详情字段 -->
        <dl class="detail-grid">
          <div>
            <dt>用户名</dt>
            <dd>{{ selectedUser.username }}</dd>
          </div>

          <div>
            <dt>电子邮箱</dt>
            <dd>{{ selectedUser.email || '—' }}</dd>
          </div>

          <div>
            <dt>用户角色</dt>
            <dd>{{ getUserRoleName(selectedUser) }}</dd>
          </div>

          <div>
            <dt>账号类型</dt>
            <dd>
              {{
                selectedUser.is_root
                  ? '根管理员'
                  : '普通用户'
              }}
            </dd>
          </div>

          <div>
            <dt>创建时间</dt>
            <dd>
              {{ formatTime(selectedUser.create_time) }}
            </dd>
          </div>

          <div>
            <dt>最后登录</dt>
            <dd>
              {{ formatTime(selectedUser.last_login) }}
            </dd>
          </div>
        </dl>
      </div>

      <template #footer>
        <button class="secondary-button" type="button" :disabled="detailLoading" @click="closeDetailModal">
          关闭
        </button>

        <button v-if="canResetUserPassword && selectedUser && !selectedUser.is_root" class="secondary-button"
          type="button" :disabled="detailLoading || !selectedUser"
          @click="closeDetailModal(); openPasswordModal(selectedUser);">
          <i class="bi bi-key" aria-hidden="true"></i>
          重置密码
        </button>

        <button v-if="canEditUser" class="primary-button" type="button" :disabled="detailLoading || !selectedUser
          " @click="editSelectedUser">
          <i class="bi bi-pencil" aria-hidden="true"></i>

          编辑用户
        </button>
      </template>
    </AppModal>

    <!-- ==================== 用户密码重置弹出层 ==================== -->

    <AppModal v-model="passwordModalVisible" scope-class="users-modal-scope" :title="passwordTargetUser
        ? `重置密码：${passwordTargetUser.username}`
        : '重置用户密码'
      " :width="480" :closable="!passwordResetting" :close-on-overlay="!passwordResetting"
      :close-on-escape="!passwordResetting">
      <form id="password-reset-form" class="user-form password-reset-form" novalidate
        @submit.prevent="submitPasswordReset">
        <!-- 密码重置说明 -->
        <div class="password-reset-notice">
          <i class="bi bi-exclamation-triangle" aria-hidden="true"></i>

          <span>
            密码重置成功后，该用户之前签发的登录凭证会立即失效，需要使用新密码重新登录。
          </span>
        </div>

        <div class="form-grid">
          <!-- 新密码 -->
          <label class="form-field full">
            <span class="field-label">
              新密码
              <i aria-hidden="true">*</i>
            </span>

            <input v-model="passwordResetForm.newPassword
              " type="password" maxlength="128" autocomplete="new-password" placeholder="请输入新密码" />
          </label>

          <!-- 确认新密码 -->
          <label class="form-field full">
            <span class="field-label">
              确认新密码
              <i aria-hidden="true">*</i>
            </span>

            <input v-model="passwordResetForm
                .newPasswordConfirm
              " type="password" maxlength="128" autocomplete="new-password" placeholder="请再次输入新密码" />
          </label>
        </div>
      </form>

      <template #footer>
        <button class="secondary-button" type="button" :disabled="passwordResetting" @click="closePasswordModal">
          取消
        </button>

        <button class="primary-button" type="submit" form="password-reset-form" :disabled="passwordResetting">
          <i v-if="passwordResetting" class="
          bi bi-arrow-clockwise
          button-loading
        " aria-hidden="true"></i>

          {{
            passwordResetting
              ? '正在重置...'
              : '确认重置'
          }}
        </button>
      </template>
    </AppModal>

    <!-- ==================== 状态确认弹出层 ==================== -->
    <AppModal v-model="statusModalVisible" scope-class="users-modal-scope" :title="statusModalTitle" :width="430"
      :closable="!submitting" :close-on-overlay="!submitting" :close-on-escape="!submitting">
      <div v-if="statusTargetUser" class="status-confirm">
        <div class="confirm-icon" :class="{
          enable: !statusTargetUser.is_active,
        }" aria-hidden="true">
          <i class="bi" :class="statusTargetUser.is_active
            ? 'bi-person-x'
            : 'bi-person-check'
            "></i>
        </div>

        <div>
          <h3>
            {{
              statusTargetUser.is_active
                ? `确定禁用“${statusTargetUser.username}”吗？`
                : `确定启用“${statusTargetUser.username}”吗？`
            }}
          </h3>

          <p>
            {{
              statusTargetUser.is_active
                ? '用户被禁用后将无法登录系统，你可以稍后重新启用。'
                : '用户启用后可以重新登录并访问已授权的页面。'
            }}
          </p>
        </div>
      </div>

      <template #footer>
        <button class="secondary-button" type="button" :disabled="submitting" @click="closeStatusModal">
          取消
        </button>

        <button class="confirm-button" :class="{
          danger:
            statusTargetUser?.is_active,
          success:
            !statusTargetUser?.is_active,
        }" type="button" :disabled="submitting" @click="confirmUserStatus">
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

<!-- ==================== 用户管理样式 ==================== -->
<style scoped lang="scss" src="./users.scss"></style>
<!-- ==================== 用户弹出层样式 ==================== -->

<!--
  弹出层通过 Teleport 渲染到 body 下，
  因此单独使用不带 scoped 的样式文件。

  users-modal.scss 中的全部样式都限制在
  .app-modal-overlay 内，不会影响其他页面。
-->
<style lang="scss" src="./users-modal.scss"></style>