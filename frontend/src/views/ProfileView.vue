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
          <p class="card-subtitle">Особисті дані адміністратора, їх можна змінювати.</p>

          <form class="profile-form" @submit.prevent="handlePersonalSubmit">
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
              <button type="submit" class="btn btn-primary" :disabled="savingPersonal">
                {{ savingPersonal ? 'Збереження...' : 'Зберегти зміни' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="resetForm" :disabled="savingPersonal">
                Скасувати зміни
              </button>
            </div>

            <div v-if="personalSuccessMessage" class="alert success">
              {{ personalSuccessMessage }}
            </div>
            <div v-if="personalErrorMessage" class="alert error">
              {{ personalErrorMessage }}
            </div>
          </form>
        </div>

        <!-- Login & Password Form — only for admin -->
        <div v-if="isAdmin" class="form-card">
          <h3 class="card-title">Дані для входу</h3>
          <p class="card-subtitle">Змініть логін або пароль для входу в систему.</p>

          <form class="profile-form" @submit.prevent="handleLoginSubmit">
            <div class="form-row">
              <div class="form-group">
                <label for="login">Логін</label>
                <input
                  id="login"
                  v-model="form.login"
                  type="text"
                  placeholder="Введіть новий логін"
                />
              </div>
              <div class="form-group">
                <label for="password">Пароль</label>
                <div class="password-input-wrapper">
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Введіть новий пароль"
                  />
                  <button
                    type="button"
                    class="password-toggle"
                    @click="showPassword = !showPassword"
                    title="Показати/сховати пароль"
                  >
                    <svg v-if="!showPassword" viewBox="0 0 24 24" width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="savingLogin">
                {{ savingLogin ? 'Збереження...' : 'Зберегти зміни' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="resetLoginForm" :disabled="savingLogin">
                Скасувати зміни
              </button>
            </div>

            <div v-if="loginSuccessMessage" class="alert success">
              {{ loginSuccessMessage }}
            </div>
            <div v-if="loginErrorMessage" class="alert error">
              {{ loginErrorMessage }}
            </div>
          </form>
        </div>

        <!-- Login Info Card — only for non-admin users -->
        <div v-if="!isAdmin" class="login-info-card">
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

const savingPersonal = ref(false)
const personalSuccessMessage = ref('')
const personalErrorMessage = ref('')

const savingLogin = ref(false)
const loginSuccessMessage = ref('')
const loginErrorMessage = ref('')

const profile = computed(() => authStore.user)
const avatarLoaded = ref(false)

const form = reactive({
  full_name: '',
  phone: '',
  avatar_url: '',
  login: '',
  password: ''
})

const isAdmin = computed(() => profile.value?.role === 'admin')

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
    form.login = profile.value.login || ''
    form.password = ''
  }
  personalSuccessMessage.value = ''
  personalErrorMessage.value = ''
  loginSuccessMessage.value = ''
  loginErrorMessage.value = ''
}

function resetLoginForm() {
  if (profile.value) {
    form.login = profile.value.login || ''
    form.password = ''
  }
  loginSuccessMessage.value = ''
  loginErrorMessage.value = ''
}

const showPassword = ref(false)

async function handlePersonalSubmit() {
  savingPersonal.value = true
  personalSuccessMessage.value = ''
  personalErrorMessage.value = ''

  const data = {
    full_name: form.full_name,
    phone: form.phone,
    avatar_url: form.avatar_url
  }

  const result = await authStore.updateProfile(data)

  savingPersonal.value = false

  if (result) {
    personalSuccessMessage.value = 'Особисті дані успішно оновлено!'
    setTimeout(() => {
      personalSuccessMessage.value = ''
    }, 3000)
  } else {
    personalErrorMessage.value = 'Помилка при збереженні особистих даних'
  }
}

async function handleLoginSubmit() {
  savingLogin.value = true
  loginSuccessMessage.value = ''
  loginErrorMessage.value = ''

  const data: any = {}

  if (form.login.trim()) {
    data.login = form.login.trim()
  }
  if (form.password.trim()) {
    data.password = form.password.trim()
  }

  const result = await authStore.updateProfile(data)

  savingLogin.value = false

  if (result) {
    loginSuccessMessage.value = 'Дані для входу успішно оновлено!'
    form.password = ''
    showPassword.value = false
    setTimeout(() => {
      loginSuccessMessage.value = ''
    }, 3000)
  } else {
    loginErrorMessage.value = 'Помилка при збереженні даних для входу'
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

/* Password Input Wrapper */
.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.password-input-wrapper input {
  width: 100%;
  padding: 0.6rem 2.5rem 0.6rem 0.8rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: border-color 0.2s;
  background-color: #f8fafc;
}

.password-input-wrapper input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
  background-color: white;
}

.password-toggle {
  position: absolute;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #475569;
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
