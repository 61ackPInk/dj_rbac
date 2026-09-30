<!-- ==================== 页面管理业务逻辑 ==================== -->

<script src="./pages.js"></script>

<template>
    <div class="pages-page">
        <!-- ==================== 页面标题 ==================== -->

        <header class="page-heading">
            <div>
                <h1>页面管理</h1>

                <p>
                    管理系统页面、导航图标、访问角色和启用状态。
                </p>
            </div>

            <button v-if="canCreatePage" class="primary-button" type="button" @click="openCreateModal">
                <i class="bi bi-plus-lg" aria-hidden="true"></i>

                <span>创建页面</span>
            </button>
        </header>

        <!-- ==================== 页面管理面板 ==================== -->

        <section class="page-panel">
            <!-- ==================== 搜索与筛选 ==================== -->

            <div class="toolbar">
                <div class="toolbar-left">
                    <label class="search-box">
                        <i class="bi bi-search" aria-hidden="true"></i>

                        <input v-model="keyword" type="search" placeholder="搜索页面名称、编码或路由" aria-label="搜索页面" />
                    </label>

                    <AppSelect v-model="statusFilter" class="toolbar-select" :options="statusFilterOptions" :width="132"
                        placeholder="全部状态" aria-label="按状态筛选" />
                </div>

                <div class="toolbar-right">
                    <button class="refresh-button" type="button" :disabled="loading" aria-label="刷新页面列表" title="刷新页面列表"
                        @click="loadPageData">
                        <i class="bi bi-arrow-clockwise" :class="{
                            'is-rotating': loading,
                        }" aria-hidden="true"></i>
                    </button>

                    <div class="view-switch" role="group" aria-label="页面显示方式">
                        <button class="view-button" :class="{
                            'is-active':
                                viewMode === 'list',
                        }" type="button" aria-label="列表显示" :aria-pressed="viewMode === 'list'
                            " @click="setViewMode('list')">
                            <i class="bi bi-list-ul" aria-hidden="true"></i>
                        </button>

                        <button class="view-button" :class="{
                            'is-active':
                                viewMode === 'card',
                        }" type="button" aria-label="卡片显示" :aria-pressed="viewMode === 'card'
                            " @click="setViewMode('card')">
                            <i class="bi bi-grid" aria-hidden="true"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- ==================== 结果统计 ==================== -->

            <div class="result-summary">
                <span>
                    共找到
                    <strong>
                        {{ filteredPages.length }}
                    </strong>
                    个页面
                </span>

                <span class="summary-status">
                    顶级页面 {{ rootPageCount }} 个，
                    已启用 {{ activeCount }} 个，
                    已停用 {{ disabledCount }} 个
                </span>
            </div>

            <!-- ==================== 加载状态 ==================== -->

            <div v-if="loading && pages.length === 0" class="page-state">
                <i class="
            bi bi-arrow-clockwise
            state-loading
          " aria-hidden="true"></i>

                <strong>正在加载页面</strong>
                <span>请稍候...</span>
            </div>

            <!-- ==================== 错误状态 ==================== -->

            <div v-else-if="errorMessage" class="page-state error" role="alert">
                <i class="bi bi-exclamation-circle" aria-hidden="true"></i>

                <strong>页面数据加载失败</strong>
                <span>{{ errorMessage }}</span>

                <button class="secondary-button" type="button" @click="loadPageData">
                    重新加载
                </button>
            </div>

            <!-- ==================== 空状态 ==================== -->

            <div v-else-if="
                filteredPages.length === 0
            " class="page-state">
                <i class="bi bi-window" aria-hidden="true"></i>

                <strong>没有找到页面</strong>

                <span>
                    请尝试修改搜索内容或筛选条件。
                </span>
            </div>

            <!-- ==================== 列表显示 ==================== -->

            <div v-else-if="viewMode === 'list'" class="list-view">
                <table class="page-table">
                    <thead>
                        <tr>
                            <th>页面结构</th>
                            <th>页面路由</th>
                            <th>可见角色</th>
                            <th>同级排序</th>
                            <th>状态</th>
                            <th class="action-column">操作</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="row in treeRows"
                            :key="row.page.id"
                            :class="{
                                'is-root-row': row.depth === 0,
                            }"
                        >
                            <!-- ==================== 树形页面名称 ==================== -->
                            <td>
                                <div
                                    class="page-cell tree-page-cell"
                                    :style="{
                                        '--tree-indent': `${row.depth * 30}px`,
                                        '--tree-branch-offset': `${row.depth * 30 - 18}px`,
                                    }"
                                >
                                    <!-- 子页面层级连接线 -->
                                    <span
                                        v-if="row.depth > 0"
                                        class="tree-branch"
                                        aria-hidden="true"
                                    ></span>

                                    <!-- 展开或收起子页面 -->
                                    <button
                                        v-if="row.childCount > 0"
                                        class="tree-toggle"
                                        type="button"
                                        :disabled="isFilteringTree"
                                        :aria-label="isPageExpanded(row.page.id)
                                            ? `收起 ${row.page.name}`
                                            : `展开 ${row.page.name}`"
                                        :aria-expanded="isFilteringTree || isPageExpanded(row.page.id)"
                                        @click="togglePageExpanded(row.page.id)"
                                    >
                                        <i
                                            class="bi bi-chevron-right"
                                            :class="{
                                                'is-expanded': isFilteringTree || isPageExpanded(row.page.id),
                                            }"
                                            aria-hidden="true"
                                        ></i>
                                    </button>

                                    <span
                                        v-else
                                        class="tree-toggle-placeholder"
                                        aria-hidden="true"
                                    ></span>

                                    <span class="page-avatar">
                                        <i
                                            :class="getPageIcon(row.page)"
                                            aria-hidden="true"
                                        ></i>
                                    </span>

                                    <div class="page-basic">
                                        <strong>
                                            {{ row.page.name }}
                                        </strong>

                                        <span>
                                            {{ row.page.code }}
                                        </span>

                                        <small
                                            v-if="row.childCount > 0"
                                            class="child-count"
                                        >
                                            {{ row.childCount }} 个直接子页面
                                        </small>
                                    </div>
                                </div>
                            </td>

                            <!-- 页面路由 -->
                            <td>
                                <code class="path-tag">
                                    {{ row.page.path }}
                                </code>
                            </td>

                            <!-- 可见角色 -->
                            <td>
                                <span
                                    class="roles-text"
                                    :title="getVisibleRoleNames(row.page)"
                                >
                                    {{ getVisibleRoleNames(row.page) }}
                                </span>
                            </td>

                            <!-- 同级排序 -->
                            <td>
                                <span class="sort-value">
                                    {{ row.page.sort_order }}
                                </span>
                            </td>

                            <!-- 状态 -->
                            <td>
                                <span
                                    class="status-tag"
                                    :class="row.page.is_active
                                        ? 'enabled'
                                        : 'disabled'"
                                >
                                    {{ row.page.is_active
                                        ? '已启用'
                                        : '已停用' }}
                                </span>
                            </td>

                            <!-- ==================== 页面操作 ==================== -->
                            <td class="action-column">
                                <div class="action-group">
                                    <AppActionMenu
                                        :items="getPageActionItems(row.page)"
                                        :aria-label="`打开页面 ${row.page.name} 的操作菜单`"
                                        @select="handlePageAction($event, row.page)"
                                    />
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- ==================== 卡片显示 ==================== -->

            <div v-else class="card-view grouped-card-view">
                <section
                    v-for="group in cardGroups"
                    :key="group.root.id"
                    class="page-card-group"
                >
                    <!-- ==================== 顶级页面分组 ==================== -->
                    <header class="page-group-header">
                        <div class="page-group-main">
                            <span class="group-icon">
                                <i
                                    :class="getPageIcon(group.root)"
                                    aria-hidden="true"
                                ></i>
                            </span>

                            <div class="group-title">
                                <strong>{{ group.root.name }}</strong>

                                <span>
                                    {{ group.root.code }} · {{ group.root.path }}
                                </span>
                            </div>
                        </div>

                        <div class="page-group-actions">
                            <span class="child-total">
                                {{ group.items.length }} 个子页面
                            </span>

                            <span
                                class="status-tag"
                                :class="group.root.is_active
                                    ? 'enabled'
                                    : 'disabled'"
                            >
                                {{ group.root.is_active
                                    ? '已启用'
                                    : '已停用' }}
                            </span>

                            <AppActionMenu
                                :items="getPageActionItems(group.root)"
                                :aria-label="`打开页面 ${group.root.name} 的操作菜单`"
                                @select="handlePageAction($event, group.root)"
                            />
                        </div>
                    </header>

                    <!-- ==================== 分组中的子页面 ==================== -->
                    <div
                        v-if="group.items.length"
                        class="page-group-grid"
                    >
                        <article
                            v-for="item in group.items"
                            :key="item.page.id"
                            class="page-card"
                        >
                            <!-- 卡片头部 -->
                            <header class="page-card-header">
                                <div class="page-card-person">
                                    <span class="card-avatar">
                                        <i
                                            :class="getPageIcon(item.page)"
                                            aria-hidden="true"
                                        ></i>
                                    </span>

                                    <div class="card-page-info">
                                        <strong>{{ item.page.name }}</strong>
                                        <span>{{ item.page.code }}</span>
                                    </div>
                                </div>

                                <span
                                    class="level-tag"
                                    :title="`第 ${item.depth} 层页面`"
                                >
                                    L{{ item.depth }}
                                </span>
                            </header>

                            <!-- 卡片资料 -->
                            <dl class="page-card-body">
                                <div class="card-info-row">
                                    <dt>页面路由</dt>
                                    <dd>{{ item.page.path }}</dd>
                                </div>

                                <div class="card-info-row">
                                    <dt>上级页面</dt>
                                    <dd>{{ getParentName(item.page) }}</dd>
                                </div>

                                <div class="card-info-row">
                                    <dt>可见角色</dt>
                                    <dd :title="getVisibleRoleNames(item.page)">
                                        {{ getVisibleRoleNames(item.page) }}
                                    </dd>
                                </div>

                                <div class="card-info-row">
                                    <dt>同级排序</dt>
                                    <dd>{{ item.page.sort_order }}</dd>
                                </div>
                            </dl>

                            <!-- ==================== 页面卡片操作 ==================== -->
                            <footer
                                v-if="hasPageActions"
                                class="page-card-footer"
                            >
                                <span class="status-tag" :class="item.page.is_active
                                    ? 'enabled'
                                    : 'disabled'">
                                    {{ item.page.is_active
                                        ? '已启用'
                                        : '已停用' }}
                                </span>

                                <AppActionMenu
                                    :items="getPageActionItems(item.page)"
                                    :aria-label="`打开页面 ${item.page.name} 的操作菜单`"
                                    @select="handlePageAction($event, item.page)"
                                />
                            </footer>
                        </article>
                    </div>

                    <div v-else class="group-empty">
                        <i class="bi bi-diagram-2" aria-hidden="true"></i>
                        <span>该顶级页面暂时没有子页面</span>
                    </div>
                </section>
            </div>
        </section>

        <!-- ==================== 创建与编辑页面弹出层 ==================== -->

        <AppModal v-model="formModalVisible" scope-class="pages-modal-scope" :title="formModalTitle" :width="760"
            :closable="!submitting" :close-on-overlay="!submitting" :close-on-escape="!submitting">
            <form id="page-form" class="page-form" novalidate @submit.prevent="submitPageForm">
                <div class="form-grid">
                    <!-- 页面名称 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            页面名称
                            <i aria-hidden="true">*</i>
                        </span>

                        <input v-model="pageForm.name" type="text" maxlength="100" autocomplete="off"
                            placeholder="例如：用户管理" />
                    </label>

                    <!-- 页面编码 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            页面编码
                            <i aria-hidden="true">*</i>
                        </span>

                        <input v-model="pageForm.code" type="text" maxlength="100" autocomplete="off"
                            placeholder="例如：SYSTEM_USERS" @blur="normalizePageCode" />

                        <small class="field-help">
                            以字母开头，只能使用字母、数字和下划线。
                        </small>
                    </label>

                    <!-- 页面路由 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            页面路由
                            <i aria-hidden="true">*</i>
                        </span>

                        <input v-model="pageForm.path" type="text" maxlength="255" autocomplete="off"
                            placeholder="例如：/system/users" />

                        <small class="field-help">
                            必须以 / 开头，不能包含空格。
                        </small>
                    </label>

                    <!-- 前端组件 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            前端组件
                        </span>

                        <input v-model="pageForm.component" type="text" maxlength="255" autocomplete="off"
                            placeholder="例如：views/system/users" />

                        <small class="field-help">
                            当前项目使用静态路由时可以留空。
                        </small>
                    </label>

                    <!-- 页面图标 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            页面图标
                        </span>

                        <AppSelect v-model="pageForm.icon" :options="bootstrapIconOptions" placeholder="请选择页面图标"
                            filterable />

                        <small class="field-help">
                            支持搜索中文名称或 Bootstrap 图标类名。
                        </small>
                    </label>

                    <!-- 父页面 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            父页面
                        </span>

                        <AppSelect v-model="pageForm.parentId" :options="parentPageOptions" placeholder="请选择父页面"
                            filterable />

                        <small class="field-help">
                            顶级页面会显示在顶部导航区域。
                        </small>
                    </label>

                    <!-- 页面排序 -->
                    <label v-if="isCreateMode || canUpdatePage" class="form-field">
                        <span class="field-label">
                            页面排序
                        </span>

                        <input v-model.number="pageForm.sortOrder
                            " type="number" min="0" step="1" inputmode="numeric" placeholder="请输入排序数字" />

                        <small class="field-help">
                            数字越小，显示位置越靠前。
                        </small>
                    </label>

                    <!-- 页面状态 -->
                    <!--
                    只有创建页面时可以设置初始状态。
                    编辑页面状态使用独立的状态按钮。
                    -->
                    <label v-if="isCreateMode && canChangePageStatus" class="form-field">
                        <span class="field-label">
                            页面状态
                        </span>
                        <AppSelect v-model="pageForm.isActive" :options="pageStatusOptions" placeholder="请选择页面状态" />
                    </label>

                    <!-- 可见角色 -->
                    <!-- 拥有页面角色分配权限时显示 -->
                    <label v-if="canAssignPageRole" class="form-field full">
                        <span class="field-label">
                            可见角色
                        </span>

                        <AppSelect v-model="pageForm.visibleRoleIds" :options="roleOptions" placeholder="请选择可以访问该页面的角色"
                            multiple filterable clearable />

                        <small class="field-help">
                            根管理员不受角色分配限制；普通用户必须拥有这里配置的角色。
                        </small>
                    </label>
                </div>
            </form>

            <template #footer>
                <button class="secondary-button" type="button" :disabled="submitting" @click="closeFormModal">
                    取消
                </button>

                <button class="primary-button" type="submit" form="page-form" :disabled="submitting">
                    <i v-if="submitting" class="
              bi bi-arrow-clockwise
              button-loading
            " aria-hidden="true"></i>

                    {{
                        submitting
                            ? '正在保存...'
                            : isCreateMode
                                ? '创建页面'
                                : '保存修改'
                    }}
                </button>
            </template>
        </AppModal>

        <!-- ==================== 页面详情弹出层 ==================== -->

        <AppModal v-model="detailModalVisible" scope-class="pages-modal-scope" title="页面信息" :width="680"
            :closable="!detailLoading" :close-on-overlay="!detailLoading
                " :close-on-escape="!detailLoading
                    ">
            <div v-if="detailLoading" class="detail-loading">
                <i class="bi bi-arrow-clockwise" aria-hidden="true"></i>

                <span>正在加载页面信息...</span>
            </div>

            <div v-else-if="selectedPage" class="page-detail">
                <!-- 详情头部 -->
                <header class="detail-profile">
                    <span class="detail-avatar">
                        <i :class="getPageIcon(selectedPage)
                            " aria-hidden="true"></i>
                    </span>

                    <div>
                        <h3>{{ selectedPage.name }}</h3>
                        <p>{{ selectedPage.code }}</p>
                    </div>

                    <span class="status-tag" :class="selectedPage.is_active
                        ? 'enabled'
                        : 'disabled'
                        ">
                        {{
                            selectedPage.is_active
                                ? '已启用'
                                : '已停用'
                        }}
                    </span>
                </header>

                <!-- 详情字段 -->
                <dl class="detail-grid">
                    <div>
                        <dt>页面名称</dt>
                        <dd>{{ selectedPage.name }}</dd>
                    </div>

                    <div>
                        <dt>页面编码</dt>
                        <dd>{{ selectedPage.code }}</dd>
                    </div>

                    <div>
                        <dt>页面路由</dt>
                        <dd>{{ selectedPage.path }}</dd>
                    </div>

                    <div>
                        <dt>前端组件</dt>
                        <dd>
                            {{
                                selectedPage.component ||
                                '未配置'
                            }}
                        </dd>
                    </div>

                    <div>
                        <dt>父页面</dt>
                        <dd>
                            {{ getParentName(selectedPage) }}
                        </dd>
                    </div>

                    <div>
                        <dt>页面排序</dt>
                        <dd>
                            {{ selectedPage.sort_order }}
                        </dd>
                    </div>

                    <div>
                        <dt>页面图标</dt>

                        <dd class="detail-icon-value">
                            <i :class="getPageIcon(selectedPage)
                                " aria-hidden="true"></i>

                            <span>
                                {{
                                    getPageIcon(selectedPage)
                                }}
                            </span>
                        </dd>
                    </div>

                    <div>
                        <dt>页面状态</dt>
                        <dd>
                            {{
                                selectedPage.is_active
                                    ? '已启用'
                                    : '已停用'
                            }}
                        </dd>
                    </div>

                    <div class="full">
                        <dt>可见角色</dt>

                        <dd>
                            {{
                                getVisibleRoleNames(
                                    selectedPage,
                                )
                            }}
                        </dd>
                    </div>

                    <div>
                        <dt>创建时间</dt>
                        <dd>
                            {{
                                formatTime(
                                    selectedPage.create_time,
                                )
                            }}
                        </dd>
                    </div>

                    <div>
                        <dt>更新时间</dt>
                        <dd>
                            {{
                                formatTime(
                                    selectedPage.update_time,
                                )
                            }}
                        </dd>
                    </div>
                </dl>
            </div>

            <template #footer>
                <button class="secondary-button" type="button" :disabled="detailLoading" @click="closeDetailModal">
                    关闭
                </button>

                <button v-if="canEditPage" class="primary-button" type="button" :disabled="detailLoading ||
                    !selectedPage
                    " @click="editSelectedPage">
                    <i class="bi bi-pencil" aria-hidden="true"></i>

                    编辑页面
                </button>
            </template>
        </AppModal>

        <!-- ==================== 状态确认弹出层 ==================== -->

        <AppModal v-model="statusModalVisible" scope-class="pages-modal-scope" :title="statusModalTitle" :width="430"
            :closable="!submitting" :close-on-overlay="!submitting" :close-on-escape="!submitting">
            <div v-if="statusTargetPage" class="status-confirm">
                <div class="confirm-icon" :class="{
                    enable:
                        !statusTargetPage.is_active,
                }" aria-hidden="true">
                    <i class="bi" :class="statusTargetPage.is_active
                        ? 'bi-window-x'
                        : 'bi-window-check'
                        "></i>
                </div>

                <div>
                    <h3>
                        {{
                            statusTargetPage.is_active
                                ? `确定停用“${statusTargetPage.name}”吗？`
                                : `确定启用“${statusTargetPage.name}”吗？`
                        }}
                    </h3>

                    <p>
                        {{
                            statusTargetPage.is_active
                                ? '停用后，该页面将从导航中隐藏，用户也不能再通过页面权限访问。'
                                : '启用后，该页面会根据父页面和角色配置重新显示。'
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
                        statusTargetPage?.is_active,
                    success:
                        !statusTargetPage?.is_active,
                }" type="button" :disabled="submitting" @click="confirmPageStatus">
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

<!-- ==================== 页面管理样式 ==================== -->

<style scoped lang="scss" src="./pages.scss"></style>

<!-- ==================== 页面弹出层业务样式 ==================== -->

<style lang="scss" src="./pages-modal.scss"></style>
