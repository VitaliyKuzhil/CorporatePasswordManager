<template>
  <div class="session-timer" v-if="authStore.isAuthenticated">
    <svg class="timer-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <span class="timer-text">Сесія ще {{ remainingTime }}</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const SESSION_DURATION_MS = 12 * 60 * 60 * 1000 // 12 годин у мілісекундах
const sessionStartTime = ref(Date.now())

const remainingMs = computed(() => {
  const elapsed = Date.now() - sessionStartTime.value
  const remaining = SESSION_DURATION_MS - elapsed
  return Math.max(0, remaining)
})

const remainingTime = computed(() => {
  const ms = remainingMs.value
  const hours = Math.floor(ms / (1000 * 60 * 60))
  const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60))
  
  if (hours > 0) {
    return `${hours} год ${minutes} хв`
  }
  return `${minutes} хв`
})

let timerInterval: number | null = null

onMounted(() => {
  // Якщо є токен у localStorage, припускаємо що сесія почалася коли токен був створений
  // Для точності потрібно зберігати час логіну, але поки що використовуємо поточний час
  timerInterval = window.setInterval(() => {
    // Примусово оновлюємо реактивність
    remainingTime.value
  }, 60000) // оновлювати кожну хвилину
})

onUnmounted(() => {
  if (timerInterval !== null) {
    clearInterval(timerInterval)
  }
})
</script>

<style scoped>
.session-timer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  color: #64748b;
  font-size: 0.875rem;
}

.timer-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.timer-text {
  white-space: nowrap;
}
</style>
