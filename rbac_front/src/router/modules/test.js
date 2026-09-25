export default [
  {
    path: '/test',
    name: 'test',
    component: () => import('@/views/test/test.vue'),
    meta: {
      title: '测试',
      requiresAuth: false,
    },
  },
]