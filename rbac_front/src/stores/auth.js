/* ==================== Vue 与 Pinia ==================== */

import {
  computed,
  ref,
} from 'vue'

import { defineStore } from 'pinia'

/* ==================== 项目 Store ==================== */

import { useNavigationStore } from '@/stores/navigation'

/* ==================== 登录相关接口 ==================== */

import {
  getCurrentUserApi,
  loginApi,
  logoutApi,
} from '@/api/auth'

/* ==================== Token 工具 ==================== */

import {
  clearTokens,
  getAccessToken,
  saveTokens,
} from '@/utils/token'

/* ==================== 登录状态 Store ==================== */

export const useAuthStore = defineStore(
  'auth',
  () => {
    /* ==================== 登录状态 ==================== */

    /*
     * accessToken 会在 Store 创建时，
     * 尝试从浏览器本地存储中恢复。
     */
    const accessToken = ref(
      getAccessToken(),
    )

    /*
     * 当前登录用户资料。
     *
     * 后端现在会返回：
     * {
     *   id,
     *   username,
     *   is_root,
     *   role,
     *   permission_codes,
     * }
     */
    const user = ref(null)

    /*
     * 是否已经检查过当前登录状态。
     *
     * 页面刷新后需要调用 /api/auth/me/，
     * 恢复保存在后端的最新用户资料和权限。
     */
    const initialized = ref(false)

    /*
     * 防止多个路由同时初始化时，
     * 重复请求 /api/auth/me/。
     */
    let initializePromise = null

    /* ==================== 登录状态计算 ==================== */

    // 浏览器本地是否存在 Access Token
    const hasAccessToken = computed(() => {
      return Boolean(accessToken.value)
    })

    /*
     * 当前是否已经登录。
     *
     * 必须同时存在 Token 和用户资料，
     * 才认为登录状态完整。
     */
    const isLoggedIn = computed(() => {
      return Boolean(
        accessToken.value &&
        user.value,
      )
    })

    /*
     * 当前用户是否为根管理员。
     *
     * 根管理员不需要分配具体操作权限，
     * 后端和前端都会直接放行。
     */
    const isRoot = computed(() => {
      return Boolean(user.value?.is_root)
    })

    /* ==================== 操作权限数据 ==================== */

    /*
     * 当前用户拥有的有效操作权限编码。
     *
     * 普通用户由后端返回具体权限；
     * 根管理员可能返回空数组，
     * 不能根据数组是否为空判断根管理员权限。
     */
    const permissionCodes = computed(() => {
      const codes =
        user.value?.permission_codes

      return Array.isArray(codes)
        ? codes
        : []
    })

    /* ==================== 单个权限判断 ==================== */

    /*
     * 判断当前用户是否拥有指定操作权限。
     *
     * 使用示例：
     * authStore.hasPermission('USER_CREATE')
     */
    const hasPermission = (
      permissionCode,
    ) => {
      if (
        !user.value ||
        !permissionCode
      ) {
        return false
      }

      /*
       * 根管理员自动拥有所有操作权限。
       *
       * 根管理员的 permission_codes 可以为空，
       * 因此必须优先判断 is_root。
       */
      if (isRoot.value) {
        return true
      }

      return permissionCodes.value.includes(
        permissionCode,
      )
    }

    /* ==================== 任意权限判断 ==================== */

    /*
     * 只要拥有权限列表中的任意一项，
     * 就返回 true。
     *
     * 使用示例：
     * authStore.hasAnyPermission([
     *   'ROLE_UPDATE',
     *   'ROLE_CHANGE_STATUS',
     * ])
     */
    const hasAnyPermission = (
      permissionCodeList,
    ) => {
      if (
        !Array.isArray(permissionCodeList) ||
        permissionCodeList.length === 0
      ) {
        return false
      }

      if (isRoot.value) {
        return true
      }

      return permissionCodeList.some(
        (permissionCode) => {
          return hasPermission(
            permissionCode,
          )
        },
      )
    }

    /* ==================== 全部权限判断 ==================== */

    /*
     * 只有同时拥有权限列表中的全部权限，
     * 才返回 true。
     *
     * 使用示例：
     * authStore.hasAllPermissions([
     *   'USER_LIST',
     *   'USER_DETAIL',
     * ])
     */
    const hasAllPermissions = (
      permissionCodeList,
    ) => {
      if (
        !Array.isArray(permissionCodeList) ||
        permissionCodeList.length === 0
      ) {
        return false
      }

      if (isRoot.value) {
        return true
      }

      return permissionCodeList.every(
        (permissionCode) => {
          return hasPermission(
            permissionCode,
          )
        },
      )
    }

    /* ==================== 登录 ==================== */

    const login = async (formData) => {
      /*
       * request.js 已经取出了响应中的 data，
       * 所以这里直接读取登录结果。
       */
      const result =
        await loginApi(formData)

      saveTokens(
        result.access_token,
        result.refresh_token,
      )

      accessToken.value =
        result.access_token

      /*
       * 登录接口中的 user 现在应当包含：
       * permission_codes。
       */
      user.value = result.user

      initialized.value = true

      return result
    }

    /* ==================== 获取当前用户 ==================== */

    /*
     * 重新获取当前用户资料和最新权限。
     *
     * 后续收到403或管理员修改权限后，
     * 可以调用这个方法刷新权限数据。
     */
    const fetchCurrentUser = async () => {
      const result =
        await getCurrentUserApi()

      user.value = result

      return result
    }

    /* ==================== 清除登录状态 ==================== */

    const clearSession = () => {
      clearTokens()

      /*
       * 退出登录后清空导航数据，
       * 避免下一个用户看到上一个用户的菜单。
       */
      useNavigationStore().clearPages()

      accessToken.value = ''
      user.value = null
    }

    /* ==================== 退出登录 ==================== */

    const logout = async () => {
      /*
       * 先请求后端，使当前用户之前签发的
       * Access Token 和 Refresh Token 失效。
       */
      await logoutApi()

      // 后端退出成功后再清除浏览器状态
      clearSession()
    }

    /* ==================== 初始化登录状态 ==================== */

    const initializeAuth = async () => {
      /*
       * 当前页面生命周期中已经初始化过，
       * 不再重复请求。
       */
      if (initialized.value) {
        return
      }

      /*
       * 已经存在初始化请求时，
       * 后续调用复用同一个 Promise。
       */
      if (initializePromise) {
        return initializePromise
      }

      initializePromise = (async () => {
        try {
          if (!hasAccessToken.value) {
            /*
             * 浏览器中没有 Token，
             * 不需要请求当前用户接口。
             */
            user.value = null
            return
          }

          /*
           * 页面刷新后 Pinia 内存会被清空，
           * 使用本地 Token 恢复用户及权限资料。
           */
          await fetchCurrentUser()
        } catch (error) {
          /*
           * 401 表示登录凭证已经失效。
           *
           * 403属于权限不足，
           * 不能在这里当成登录失效处理。
           */
          if (error.status === 401) {
            clearSession()
          }

          throw error
        } finally {
          initialized.value = true
          initializePromise = null
        }
      })()

      return initializePromise
    }

    /* ==================== Store 对外内容 ==================== */

    return {
      // 登录状态
      accessToken,
      user,
      initialized,
      hasAccessToken,
      isLoggedIn,
      isRoot,

      // 操作权限
      permissionCodes,
      hasPermission,
      hasAnyPermission,
      hasAllPermissions,

      // 登录操作
      login,
      logout,
      fetchCurrentUser,
      initializeAuth,
      clearSession,
    }
  },
)