<script setup>
import { RouterView } from 'vue-router'
import AppMessage from '@/components/feedback/message/message.vue'
</script>

<template>
  <!-- 根据当前网址，显示对应的页面组件 -->
  <RouterView />
  <AppMessage />
</template>