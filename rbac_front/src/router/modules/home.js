export default [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/home/index.vue'),
    meta: {
      title: '首页',
      requiresAuth: true,
    },
  },
  /*
     * 以后新增页面，重复以下步骤：
     * 1. 在 src/views 创建对应的 .vue 文件。
     * 2. 在 routes 添加 path、唯一 name 和 component。
     * 3. 填写 meta.title。
     * 4. 需要登录的页面设置 requiresAuth: true。
     *
     * requiresAuth 只控制登录入口，不是角色权限校验。
     * 页面和卡片权限后续按后端返回的授权配置处理。
     */
]