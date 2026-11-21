<template>
  <header class="topbar">
    <h1 class="topbar-title" @click="goHome">{{ title }}</h1>
    <div class="topbar-actions">
      <div class="profile-dropdown" v-if="authStore.user">
        <button class="profile-btn" @click="toggleProfileMenu">
          <span class="avatar">{{ getInitials(authStore.user.login) }}</span>
          <span class="username">{{ authStore.user.login }}</span>
          <span class="arrow" :class="{ open: showProfileMenu }">▼</span>
        </button>
        <div class="dropdown-menu" v-if="showProfileMenu">
          <div class="dropdown-header">
            <div class="dropdown-login">{{ authStore.user.login }}</div>
            <div class="dropdown-role">{{ authStore.user.role }}</div>
          </div>
          <hr class="dropdown-divider">
          <button class="dropdown-item" @click="goToProfile">
            <span class="dropdown-icon">👤</span> Профіль
          </button>
          <button class="dropdown-item logout" @click="handleLogout">
            <span class="dropdown-icon">🚪</span> Вийти
          </button>
        </div>
      </div>
      <button v-else class="profile-btn loading">
        <span class="username">Завантаження...</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

defineProps<{
  title?: string
}>()

const router = useRouter()
const authStore = useAuthStore()
const showProfileMenu = ref(false)

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchProfile()
  }
})

const toggleProfileMenu = () => {
  showProfileMenu.value = !showProfileMenu.value
}

const closeProfileMenu = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.profile-dropdown')) {
    showProfileMenu.value = false
  }
}

const getInitials = (login: string) => {
  return login.charAt(0).toUpperCase()
}

const goToProfile = () => {
  showProfileMenu.value = false
  router.push({ name: 'profile' })
}

const goHome = () => {
  router.push({ name: 'home' })
}

const handleLogout = () => {
  showProfileMenu.value = false
  authStore.logout()
  router.push({ name: 'login' })
}

document.addEventListener('click', closeProfileMenu)
onUnmounted(() => {
  document.removeEventListener('click', closeProfileMenu)
})
</script>

<style scoped>
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
}

.topbar h1 {
  margin: 0;
  font-size: 1.25rem;
  cursor: pointer;
  user-select: none;
  transition: opacity 0.2s;
}

.topbar-title:hover {
  opacity: 0.8;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.profile-dropdown {
  position: relative;
}

.profile-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.profile-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.profile-btn.loading {
  cursor: default;
  opacity: 0.7;
}

.avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background-color: #3498db;
  border-radius: 50%;
  font-weight: bold;
  font-size: 0.85rem;
}

.username {
  font-weight: 500;
}

.arrow {
  font-size: 0.6rem;
  transition: transform 0.2s;
}

.arrow.open {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  z-index: 100;
  overflow: hidden;
}

.dropdown-header {
  padding: 1rem;
  background-color: #f8f9fa;
}

.dropdown-login {
  font-weight: 600;
  color: #2c3e50;
  font-size: 0.95rem;
}

.dropdown-role {
  color: #7f8c8d;
  font-size: 0.85rem;
  margin-top: 0.2rem;
}

.dropdown-divider {
  border: none;
  border-top: 1px solid #ecf0f1;
  margin: 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
  color: #2c3e50;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.logout {
  color: #e74c3c;
}

.dropdown-item.logout:hover {
  background-color: #fdf2f2;
}

.dropdown-icon {
  font-size: 1rem;
}
</style>
