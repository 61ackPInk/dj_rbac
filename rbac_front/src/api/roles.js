import request from '@/utils/request'

// 已登录用户：获取角色列表
export const getRolesApi = () =>
  request({
    url: '/roles/',
    method: 'get',
  })