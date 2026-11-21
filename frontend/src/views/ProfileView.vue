<template>
  <div class="profile-page">
      <div class="profile-card" v-if="profile">
        <div class="profile-header">
          <div class="avatar-large">
            {{ getInitials(profile.login) }}
          </div>
          <div class="profile-meta">
            <div class="profile-login">{{ profile.login }}</div>
            <div class="profile-role">{{ getRoleLabel(profile.role) }}</div>
            <div class="profile-status" :class="profile.status">
              {{ getStatusLabel(profile.status) }}
            </div>
          </div>
        </div>

        <form class="profile-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="full_name">Повне ім'я</label>
            <input
              id="full_name"
              v-model="form.full_name"
              type="text"
              placeholder="Введіть ваше ім'я"
            />
          </div>

          <div class="form-group">
            <label for="phone">Телефон</label>
            <input
              id="phone"
              v-model="form.phone"
              type="tel"
              placeholder="+380 XX XXX XX XX"
            />
          </div>

          <div class="form-group">
            <label for="avatar_url">URL аватара</label>
            <input
              id="avatar_url"
              v-model="form.avatar_url"
              type="url"
              placeholder="https://example.com/avatar.jpg"
            />
          </div>


          <div class="form-actions">
            <button type="submit" class="btn-save" :disabled="saving">
              {{ saving ? 'Збереження...' : 'Зберегти' }}
            </button>
            <button type="button" class="btn-cancel" @click="resetForm" :disabled="saving">
              Скасувати зміни
            </button>
            <button class="back-btn" @click="goBack">Повернутися на головну</button>
          </div>

          <div v-if="successMessage" class="alert success">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="alert error">
            {{ errorMessage }}
          </div>
        </form>
      </div>

      <div class="profile-card loading" v-else>
        <p>Завантаження профілю...</p>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const saving = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const profile = computed(() => authStore.user)

const form = reactive({
  full_name: '',
  phone: '',
  avatar_url: '',
  status: 'active'
})

function getInitials(login: string) {
  return login.charAt(0).toUpperCase()
}

function getRoleLabel(role: string | null) {
  if (!role) return 'Користувач'
  if (role === 'admin') return 'Адміністратор'
  return 'Користувач'
}

function getStatusLabel(status: string | null) {
  if (!status) return 'Активний'
  if (status === 'active') return 'Активний'
  if (status === 'blocked') return 'Заблокований'
  return status
}

function resetForm() {
  if (profile.value) {
    form.full_name = profile.value.full_name || ''
    form.phone = profile.value.phone || ''
    form.avatar_url = profile.value.avatar_url || ''
    form.status = profile.value.status || 'active'
  }
  successMessage.value = ''
  errorMessage.value = ''
}

async function handleSubmit() {
  saving.value = true
  successMessage.value = ''
  errorMessage.value = ''

  const result = await authStore.updateProfile({
    full_name: form.full_name,
    phone: form.phone,
    avatar_url: form.avatar_url
  })

  saving.value = false

  if (result) {
    successMessage.value = 'Профіль успішно оновлено!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } else {
    errorMessage.value = 'Помилка при збереженні профілю'
  }
}

function goBack() {
  router.push({ name: 'home' })
}

onMounted(() => {
  if (authStore.isAuthenticated && !authStore.user) {
    authStore.fetchProfile()
  }
  resetForm()
})
</script>

<style scoped>
.profile-page {
  max-width: 800px;
}

.profile-card {
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  padding: 2rem;
}

.profile-card.loading {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eee;
}

.avatar-large {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  flex-shrink: 0;
}

.profile-meta {
  flex: 1;
}

.profile-login {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2c3e50;
}

.profile-role {
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.profile-status {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.profile-status.active {
  background-color: #d4edda;
  color: #155724;
}

.profile-status.blocked {
  background-color: #f8d7da;
  color: #721c24;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 0.6rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.btn-save {
  padding: 0.6rem 1.5rem;
  background-color: #155724;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-save:hover:not(:disabled) {
  background-color: darkolivegreen;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  padding: 0.6rem 1.5rem;
  background-color: #ecf0f1;
  color: #2c3e50;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-cancel:hover:not(:disabled) {
  background-color: #bdc3c7;
}

.btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  padding: 0.8rem 1rem;
  border-radius: 4px;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.alert.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.alert.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
