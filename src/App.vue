<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  // 初始化用户信息
  userStore.initializeUser()
})
</script>

<style scoped>
#app {
  height: 100vh;
  overflow: hidden;
}
</style>
