import request from '@/utils/request'

/*
 * 新增接口时，重复以下方式：
 * 1. 在 src/api 下找到对应业务文件，没有就创建。
 * 2. 导入公共 request。
 * 3. 导出一个函数，填写 url、method 和参数。
 * 4. 页面导入该函数并调用，不在页面里重复写 Axios 配置。
 */

// 注册用户：data 是提交给后端的注册信息
export const registerApi = (data) => {
  return request({
    url: '/auth/register/',
    method: 'post',
    data,
  })
}

// 登录：data 包含 username 和 password
export const loginApi = (data) => {
  return request({
    url: '/auth/login/',
    method: 'post',
    data,
  })
}

// 获取当前用户：后续需要携带 access_token
export const getCurrentUserApi = () => {
  return request({
    url: '/auth/me/',
    method: 'get',
  })
}

// 退出登录 
export const logoutApi = () => {
  return request({
    url: '/auth/logout/',
    method: 'post',
  })
}