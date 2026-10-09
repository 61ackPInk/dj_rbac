<script setup>
/* ==================== Vue 与路由 ==================== */

import {
  onBeforeUnmount,
  onMounted,
} from 'vue'

import {
  RouterView,
  useRouter,
} from 'vue-router'

/* ==================== 公共消息组件 ==================== */

import AppMessage from '@/components/feedback/message/message.vue'

/* ==================== 用户和导航状态 ==================== */

import { useAuthStore } from '@/stores/auth'
import { useNavigationStore } from '@/stores/navigation'

/* ==================== 页面依赖 ==================== */

const router = useRouter()
const authStore = useAuthStore()
const navigationStore =
  useNavigationStore()

/* ==================== 权限同步状态 ==================== */

/*
 * 多个接口可能同时返回403。
 *
 * 使用同一个 Promise 合并同步操作，
 * 避免重复请求当前用户和菜单接口。
 */
let permissionSyncPromise = null

/* ==================== 检查当前页面权限 ==================== */

const checkCurrentPageAccess = () => {
  const currentRoute =
    router.currentRoute.value

  const pageCode =
    currentRoute.meta.pageCode

  /*
   * 首页、登录页等没有 pageCode 的页面，
   * 不需要进行数据库页面权限判断。
   */
  if (!pageCode) {
    return
  }

  const canAccessCurrentPage =
    navigationStore.pages.some((page) => {
      return page.code === pageCode
    })

  /*
   * 当前页面权限已经被撤销时，
   * 返回固定首页。
   */
  if (!canAccessCurrentPage) {
    router.replace({
      name: 'home',
    })
  }
}

/* ==================== 同步当前权限与菜单 ==================== */

const synchronizePermissions = async () => {
  /*
   * 已经存在同步任务时，
   * 后续403复用同一个任务。
   */
  if (permissionSyncPromise) {
    return permissionSyncPromise
  }

  permissionSyncPromise = (async () => {
    try {
      /*
       * 重新获取：
       *
       * 1. 当前用户及 permission_codes；
       * 2. 当前用户可见页面。
       */
      await authStore.fetchCurrentUser()

      navigationStore.clearPages()
      await navigationStore.loadPages()

      /*
       * 权限更新后检查当前路由。
       */
      checkCurrentPageAccess()
    } catch (error) {
      /*
       * 401会由请求拦截器处理并跳转登录页。
       *
       * 这里不重复弹出消息，
       * 原业务操作已经会显示后端错误。
       */
      console.warn(
        '同步用户权限失败：',
        error,
      )
    } finally {
      permissionSyncPromise = null
    }
  })()

  return permissionSyncPromise
}

/* ==================== 403事件处理 ==================== */

const handlePermissionDenied = () => {
  synchronizePermissions()
}

/* ==================== 注册与移除事件 ==================== */

onMounted(() => {
  window.addEventListener(
    'rbac:permission-denied',
    handlePermissionDenied,
  )
})

onBeforeUnmount(() => {
  window.removeEventListener(
    'rbac:permission-denied',
    handlePermissionDenied,
  )
})
</script>

<template>
  <!-- ==================== 当前路由页面 ==================== -->

  <RouterView />

  <!-- ==================== 全局消息提示 ==================== -->

  <AppMessage />
</template>