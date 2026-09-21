<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useNavigationStore } from '@/stores/navigation'

const route = useRoute()
const navigationStore = useNavigationStore()

const currentPage = computed(() =>
  navigationStore.pages.find(
    (page) => page.path === route.path,
  ),
)
</script>

<template>
  <section class="page-placeholder">
    <h1>{{ currentPage?.name || '页面未找到' }}</h1>
    <p v-if="currentPage">这个页面的功能尚未开发。</p>
    <p v-else>当前地址不在你的可见页面列表中。</p>
  </section>
</template>