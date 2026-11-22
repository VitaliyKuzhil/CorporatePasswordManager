<template>
  <div class="profile-page">
    <div class="profile-layout" v-if="profile">
      <!-- Left Info Card -->
      <div class="info-card">
        <div class="avatar-wrapper">
          <img
            v-if="profile.avatar_url && avatarLoaded"
            :src="profile.avatar_url"
            alt="Аватар"
            class="avatar-img"
            @load="avatarLoaded = true"
            @error="avatarLoaded = false"
          />
          <div v-else class="avatar-placeholder">
            {{ getInitials(profile.full_name || profile.login) }}
          </div>
        </div>
        <h2 class="info-name">{{ profile.full_name || profile.login }}</h2>
        <p class="info-role">{{ getRoleLabel(profile.role) }}</p>
        <div class="info-status" :class="profile.status">
          {{ getStatusLabel(profile.status) }}
        </div>
        <div class="info-details">
          <div class="info-row">
            <span class="info-label">Логін</span>
            <span class="info-value">{{ profile.login }}</span>
          </div>
          <div class="info-row" v-if="profile.phone">
            <span class="info-label">Телефон</span>
            <span class="info-value">{{ profile.phone }}</span>
          </div>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-content">
        <!-- Personal Info Form -->
        <div class="form-card">
          <h3 class="card-title">Особисті дані</h3>
          <p class="card-subtitle">Ці дані бачить адміністратор, їх можна змінювати.</p>

          <form class="profile-form" @submit.prevent="handleSubmit">
            <div class="form-row">
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
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Збереження...' : 'Зберегти зміни' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="resetForm" :disabled="saving">
                Скасувати зміни
              </button>
              <button type="button" class="btn btn-ghost" @click="goBack">
                На головну
              </button>
            </div>

            <div v-if="successMessage" class="alert success">
              {{ successMessage }}
            </div>
            <div v-if="errorMessage" class="alert error">
              {{ errorMessage }}
            </div>
          </form>
        </div>

        <!-- Login Info Card -->
        <div class="login-info-card">
          <div class="login-info-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M19 12C19 15.866 15.866 19 12 19C8.13401 19 5 15.866 5 12C5 8.13401 8.13401 5 12 5C15.866 5 19 8.13401 19 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M6 12V10C6 7.79086 7.79086 6 10 6H14C16.2091 6 18 7.79086 18 10V12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="login-info-content">
            <h4 class="login-info-title">Дані для входу</h4>
            <p class="login-info-text">
              Логін і пароль для входу змінює лише адміністратор. Якщо їх потрібно змінити, зверніться до нього.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="profile-page loading" v-else>
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
const avatarLoaded = ref(false)

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
  if (authStore.user?.role === 'admin') {
    router.push({ name: 'services' })
  } else {
    router.push({ name: 'home' })
  }
}

onMounted(() => {
  resetForm()
})
</script>

<style scoped>
.profile-page {
  width: 100%;
}

.profile-page.loading {
  text-align: center;
  padding: 3rem;
  color: #999;
}

/* Layout */
.profile-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
  align-items: start;
}

/* Left Info Card */
.info-card {
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  padding: 2rem;
  text-align: center;
}

.avatar-wrapper {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: #0d9488;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.info-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem;
}

.info-role {
  color: #64748b;
  font-size: 0.85rem;
  margin: 0 0 0.5rem;
}

.info-status {
  display: inline-block;
  padding: 0.2rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}

.info-status.active {
  background-color: #d1fae5;
  color: #065f46;
}

.info-status.blocked {
  background-color: #fee2e2;
  color: #991b1b;
}

.info-details {
  text-align: left;
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.info-row {
  margin-bottom: 0.75rem;
}

.info-label {
  display: block;
  font-size: 0.7rem;
  color: #94a3b8;
  margin-bottom: 0.125rem;
}

.info-value {
  font-size: 0.85rem;
  color: #334155;
  font-weight: 500;
}

/* Right Content */
.right-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Form Card */
.form-card {
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem;
}

.card-subtitle {
  font-size: 0.8rem;
  color: #94a3b8;
  margin: 0 0 1.5rem;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-weight: 500;
  color: #475569;
  font-size: 0.8rem;
}

.form-group input {
  padding: 0.6rem 0.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: border-color 0.2s;
  background-color: #f8fafc;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  background-color: white;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
  align-items: center;
}

.btn {
  padding: 0.5rem 1.25rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #065f46;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #047857;
}

.btn-secondary {
  background-color: #f1f5f9;
  color: #334155;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #e2e8f0;
}

.btn-ghost {
  background: transparent;
  color: #64748b;
  margin-left: auto;
}

.btn-ghost:hover {
  color: #334155;
  background-color: #f1f5f9;
}

/* Login Info Card */
.login-info-card {
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  padding: 1.25rem 1.5rem;
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.login-info-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.75rem;
  background-color: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.login-info-icon svg {
  width: 20px;
  height: 20px;
}

.login-info-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem;
}

.login-info-text {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

/* Alerts */
.alert {
  padding: 0.8rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.alert.success {
  background-color: #d1fae5;
  color: #065f46;
  border: 1px solid #a7f3d0;
}

.alert.error {
  background-color: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

/* Responsive */
@media (max-width: 900px) {
  .profile-layout {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
