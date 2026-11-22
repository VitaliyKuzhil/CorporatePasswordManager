<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import Sidebar from '@/components/Sidebar.vue'

const route = useRoute()

const isLogin = computed(() => route.name === 'login')
</script>

<template>
  <div :class="{ 'login-layout': isLogin }">
    <div v-if="!isLogin" class="app-layout">
      <Sidebar />
      <div class="main-area">
        <main class="content">
          <RouterView />
        </main>
      </div>
    </div>
    <RouterView v-if="isLogin" />
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: #f1f5f9;
}

.content {
  flex: 1;
  padding: 2rem 2rem 2rem;
  overflow-y: auto;
}

.login-layout {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
