import request from '@/utils/request'

// 根管理员：获取用户列表
export const getUsersApi = () =>
  request({
    url: '/users/',
    method: 'get',
  })