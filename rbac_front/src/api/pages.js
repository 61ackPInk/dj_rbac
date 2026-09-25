import request from '@/utils/request'

// 获取当前用户有权查看的页面
export const getVisiblePagesApi = () => {
  return request({
    url: '/pages/visible/',
    method: 'get',
  })
}