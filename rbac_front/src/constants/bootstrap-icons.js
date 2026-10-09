/* ==================== 页面默认图标 ==================== */

/*
 * 页面没有配置图标时使用的默认图标。
 */
export const DEFAULT_PAGE_ICON =
  'bi bi-file-earmark'

/* ==================== Bootstrap 页面图标选项 ==================== */

/*
 * 公共页面图标选项。
 *
 * label：
 * AppSelect 显示和搜索的文字。
 *
 * value：
 * 保存到数据库 icon 字段的值。
 *
 * icon：
 * AppSelect 在选项中显示的图标。
 *
 * description：
 * 下拉选项右侧显示的 Bootstrap 图标类名。
 *
 * label 中同时包含中文名称和 Bootstrap 类名，
 * 因此可以搜索：
 *
 * 用户
 * people
 * bi-people
 */
export const bootstrapIconOptions = [
  /* ==================== 首页与导航 ==================== */

  {
    label: '首页 · bi-house',
    value: 'bi bi-house',
    icon: 'bi bi-house',
    description: 'bi-house',
  },
  {
    label: '首页填充 · bi-house-fill',
    value: 'bi bi-house-fill',
    icon: 'bi bi-house-fill',
    description: 'bi-house-fill',
  },
  {
    label: '应用网格 · bi-grid',
    value: 'bi bi-grid',
    icon: 'bi bi-grid',
    description: 'bi-grid',
  },
  {
    label: '应用网格填充 · bi-grid-fill',
    value: 'bi bi-grid-fill',
    icon: 'bi bi-grid-fill',
    description: 'bi-grid-fill',
  },
  {
    label: '仪表盘 · bi-speedometer2',
    value: 'bi bi-speedometer2',
    icon: 'bi bi-speedometer2',
    description: 'bi-speedometer2',
  },
  {
    label: '列表 · bi-list-ul',
    value: 'bi bi-list-ul',
    icon: 'bi bi-list-ul',
    description: 'bi-list-ul',
  },
  {
    label: '菜单 · bi-menu-button-wide',
    value: 'bi bi-menu-button-wide',
    icon: 'bi bi-menu-button-wide',
    description: 'bi-menu-button-wide',
  },

  /* ==================== 用户与权限 ==================== */

  {
    label: '用户 · bi-person',
    value: 'bi bi-person',
    icon: 'bi bi-person',
    description: 'bi-person',
  },
  {
    label: '用户填充 · bi-person-fill',
    value: 'bi bi-person-fill',
    icon: 'bi bi-person-fill',
    description: 'bi-person-fill',
  },
  {
    label: '用户组 · bi-people',
    value: 'bi bi-people',
    icon: 'bi bi-people',
    description: 'bi-people',
  },
  {
    label: '用户组填充 · bi-people-fill',
    value: 'bi bi-people-fill',
    icon: 'bi bi-people-fill',
    description: 'bi-people-fill',
  },
  {
    label: '身份角色 · bi-person-badge',
    value: 'bi bi-person-badge',
    icon: 'bi bi-person-badge',
    description: 'bi-person-badge',
  },
  {
    label: '用户配置 · bi-person-gear',
    value: 'bi bi-person-gear',
    icon: 'bi bi-person-gear',
    description: 'bi-person-gear',
  },
  {
    label: '用户锁定 · bi-person-lock',
    value: 'bi bi-person-lock',
    icon: 'bi bi-person-lock',
    description: 'bi-person-lock',
  },
  {
    label: '权限验证 · bi-shield-check',
    value: 'bi bi-shield-check',
    icon: 'bi bi-shield-check',
    description: 'bi-shield-check',
  },
  {
    label: '安全锁 · bi-shield-lock',
    value: 'bi bi-shield-lock',
    icon: 'bi bi-shield-lock',
    description: 'bi-shield-lock',
  },
  {
    label: '钥匙 · bi-key',
    value: 'bi bi-key',
    icon: 'bi bi-key',
    description: 'bi-key',
  },
  {
    label: '锁定 · bi-lock',
    value: 'bi bi-lock',
    icon: 'bi bi-lock',
    description: 'bi-lock',
  },
  {
    label: '解锁 · bi-unlock',
    value: 'bi bi-unlock',
    icon: 'bi bi-unlock',
    description: 'bi-unlock',
  },

  /* ==================== 系统与设置 ==================== */

  {
    label: '系统设置 · bi-gear',
    value: 'bi bi-gear',
    icon: 'bi bi-gear',
    description: 'bi-gear',
  },
  {
    label: '系统设置填充 · bi-gear-fill',
    value: 'bi bi-gear-fill',
    icon: 'bi bi-gear-fill',
    description: 'bi-gear-fill',
  },
  {
    label: '工具 · bi-tools',
    value: 'bi bi-tools',
    icon: 'bi bi-tools',
    description: 'bi-tools',
  },
  {
    label: '调节器 · bi-sliders',
    value: 'bi bi-sliders',
    icon: 'bi bi-sliders',
    description: 'bi-sliders',
  },
  {
    label: '服务器 · bi-server',
    value: 'bi bi-server',
    icon: 'bi bi-server',
    description: 'bi-server',
  },
  {
    label: '数据库 · bi-database',
    value: 'bi bi-database',
    icon: 'bi bi-database',
    description: 'bi-database',
  },
  {
    label: '硬盘 · bi-hdd',
    value: 'bi bi-hdd',
    icon: 'bi bi-hdd',
    description: 'bi-hdd',
  },
  {
    label: '云服务 · bi-cloud',
    value: 'bi bi-cloud',
    icon: 'bi bi-cloud',
    description: 'bi-cloud',
  },

  /* ==================== 页面与文件 ==================== */

  {
    label: '页面 · bi-file-earmark',
    value: 'bi bi-file-earmark',
    icon: 'bi bi-file-earmark',
    description: 'bi-file-earmark',
  },
  {
    label: '文本页面 · bi-file-earmark-text',
    value: 'bi bi-file-earmark-text',
    icon: 'bi bi-file-earmark-text',
    description: 'bi-file-earmark-text',
  },
  {
    label: '代码页面 · bi-file-earmark-code',
    value: 'bi bi-file-earmark-code',
    icon: 'bi bi-file-earmark-code',
    description: 'bi-file-earmark-code',
  },
  {
    label: '文件夹 · bi-folder',
    value: 'bi bi-folder',
    icon: 'bi bi-folder',
    description: 'bi-folder',
  },
  {
    label: '文件夹填充 · bi-folder-fill',
    value: 'bi bi-folder-fill',
    icon: 'bi bi-folder-fill',
    description: 'bi-folder-fill',
  },
  {
    label: '浏览器窗口 · bi-window',
    value: 'bi bi-window',
    icon: 'bi bi-window',
    description: 'bi-window',
  },
  {
    label: '页面集合 · bi-collection',
    value: 'bi bi-collection',
    icon: 'bi bi-collection',
    description: 'bi-collection',
  },
  {
    label: '层级 · bi-layers',
    value: 'bi bi-layers',
    icon: 'bi bi-layers',
    description: 'bi-layers',
  },
  {
    label: '关系结构 · bi-diagram-3',
    value: 'bi bi-diagram-3',
    icon: 'bi bi-diagram-3',
    description: 'bi-diagram-3',
  },

  /* ==================== 数据与报表 ==================== */

  {
    label: '柱状图 · bi-bar-chart',
    value: 'bi bi-bar-chart',
    icon: 'bi bi-bar-chart',
    description: 'bi-bar-chart',
  },
  {
    label: '增长趋势 · bi-graph-up',
    value: 'bi bi-graph-up',
    icon: 'bi bi-graph-up',
    description: 'bi-graph-up',
  },
  {
    label: '饼图 · bi-pie-chart',
    value: 'bi bi-pie-chart',
    icon: 'bi bi-pie-chart',
    description: 'bi-pie-chart',
  },
  {
    label: '统计面板 · bi-clipboard-data',
    value: 'bi bi-clipboard-data',
    icon: 'bi bi-clipboard-data',
    description: 'bi-clipboard-data',
  },
  {
    label: '表格 · bi-table',
    value: 'bi bi-table',
    icon: 'bi bi-table',
    description: 'bi-table',
  },

  /* ==================== 业务功能 ==================== */

  {
    label: '商品 · bi-box',
    value: 'bi bi-box',
    icon: 'bi bi-box',
    description: 'bi-box',
  },
  {
    label: '商品集合 · bi-boxes',
    value: 'bi bi-boxes',
    icon: 'bi bi-boxes',
    description: 'bi-boxes',
  },
  {
    label: '购物车 · bi-cart',
    value: 'bi bi-cart',
    icon: 'bi bi-cart',
    description: 'bi-cart',
  },
  {
    label: '商店 · bi-shop',
    value: 'bi bi-shop',
    icon: 'bi bi-shop',
    description: 'bi-shop',
  },
  {
    label: '标签 · bi-tags',
    value: 'bi bi-tags',
    icon: 'bi bi-tags',
    description: 'bi-tags',
  },
  {
    label: '钱包 · bi-wallet2',
    value: 'bi bi-wallet2',
    icon: 'bi bi-wallet2',
    description: 'bi-wallet2',
  },
  {
    label: '收据 · bi-receipt',
    value: 'bi bi-receipt',
    icon: 'bi bi-receipt',
    description: 'bi-receipt',
  },
  {
    label: '办公包 · bi-briefcase',
    value: 'bi bi-briefcase',
    icon: 'bi bi-briefcase',
    description: 'bi-briefcase',
  },
  {
    label: '建筑 · bi-building',
    value: 'bi bi-building',
    icon: 'bi bi-building',
    description: 'bi-building',
  },
  {
    label: '运输 · bi-truck',
    value: 'bi bi-truck',
    icon: 'bi bi-truck',
    description: 'bi-truck',
  },

  /* ==================== 消息与时间 ==================== */

  {
    label: '通知 · bi-bell',
    value: 'bi bi-bell',
    icon: 'bi bi-bell',
    description: 'bi-bell',
  },
  {
    label: '邮件 · bi-envelope',
    value: 'bi bi-envelope',
    icon: 'bi bi-envelope',
    description: 'bi-envelope',
  },
  {
    label: '聊天 · bi-chat-dots',
    value: 'bi bi-chat-dots',
    icon: 'bi bi-chat-dots',
    description: 'bi-chat-dots',
  },
  {
    label: '日历 · bi-calendar',
    value: 'bi bi-calendar',
    icon: 'bi bi-calendar',
    description: 'bi-calendar',
  },
  {
    label: '时间 · bi-clock',
    value: 'bi bi-clock',
    icon: 'bi bi-clock',
    description: 'bi-clock',
  },

  /* ==================== 其他常用图标 ==================== */

  {
    label: '搜索 · bi-search',
    value: 'bi bi-search',
    icon: 'bi bi-search',
    description: 'bi-search',
  },
  {
    label: '链接 · bi-link-45deg',
    value: 'bi bi-link-45deg',
    icon: 'bi bi-link-45deg',
    description: 'bi-link-45deg',
  },
  {
    label: '全球 · bi-globe',
    value: 'bi bi-globe',
    icon: 'bi bi-globe',
    description: 'bi-globe',
  },
  {
    label: '归档 · bi-archive',
    value: 'bi bi-archive',
    icon: 'bi bi-archive',
    description: 'bi-archive',
  },
  {
    label: '日志 · bi-journal-text',
    value: 'bi bi-journal-text',
    icon: 'bi bi-journal-text',
    description: 'bi-journal-text',
  },
  {
    label: '帮助 · bi-question-circle',
    value: 'bi bi-question-circle',
    icon: 'bi bi-question-circle',
    description: 'bi-question-circle',
  },
  {
    label: '信息 · bi-info-circle',
    value: 'bi bi-info-circle',
    icon: 'bi bi-info-circle',
    description: 'bi-info-circle',
  },
]