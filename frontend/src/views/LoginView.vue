<template>
  <div class="login-page">
    <!-- Ліва панель — брендинг -->
    <div class="login-left">
      <div class="left-content">
        <div class="brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="currentColor" width="28" height="28">
              <path d="M12 2C9.243 2 7 4.243 7 7v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V7c0-2.757-2.243-5-5-5zm0 2c1.654 0 3 1.346 3 3v3H9V7c0-1.654 1.346-3 3-3zm-5 8h10v8H7v-8z"/>
            </svg>
          </div>
          <span class="brand-name">Corporate Password Manager</span>
        </div>

        <h1 class="tagline">
          Усі робочі доступи<br>— в одному захищеному місці
        </h1>
        <p class="tagline-sub">
          Зберігайте, знаходьте та передавайте корпоративні паролі без листування та таблиць.
        </p>

        <ul class="features">
          <li class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
            <div class="feature-text">
              <strong>Лише зашифровані паролі</strong>
              <span>Усі записи зберігаються в базі виключно в зашифрованому вигляді.</span>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
              </svg>
            </div>
            <div class="feature-text">
              <strong>Доступ видає адміністратор</strong>
              <span>Ви бачите тільки ті паролі, до яких вам надано дозвіл.</span>
            </div>
          </li>
          <li class="feature-item">
            <div class="feature-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="20" height="20">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <div class="feature-text">
              <strong>Сесія діє 12 годин</strong>
              <span>Після цього система попросить увійти знову.</span>
            </div>
          </li>
        </ul>

        <p class="footer-note">Внутрішня система компанії. Доступ лише для співробітників.</p>
      </div>
    </div>

    <!-- Права панель — форма входу -->
    <div class="login-right">
      <div class="login-card">
        <h2>Вхід до системи</h2>
        <p class="subtitle">Введіть логін і пароль, які видав адміністратор.</p>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="username">Логін</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="a.metlyuk"
                required
              />
            </div>
          </div>

          <div class="form-group">
            <label for="password">Пароль</label>
            <div class="input-wrapper">
              <svg class="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="••••••••••"
                required
              />
            </div>
          </div>

          <div v-if="authStore.error" class="error-message">
            {{ authStore.error }}
          </div>

          <button type="submit" :disabled="isLoading" class="login-btn">
            <span>{{ isLoading ? 'Зачекайте...' : 'Увійти' }}</span>
            <svg v-if="!isLoading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12 5 19 12 12 19"/>
            </svg>
          </button>
        </form>

        <div class="info-note">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          <p>Немає облікового запису або забули пароль? Зверніться до адміністратора: самостійної реєстрації в системі немає.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  const success = await authStore.login(username.value, password.value)
  isLoading.value = false

  if (success) {
    router.push('/') // Перехід на головну після успішного входу
  }
}

// Якщо вже авторизований, перенаправити на головну
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/')
  }
})
</script>

<style scoped>
/* === Split screen layout === */
.login-page {
  display: flex;
  width: 100%;
  height: 100%;
  min-height: 100vh;
}

/* === Left panel — branding === */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.login-left::after {
  content: '';
  position: absolute;
  bottom: -60px;
  right: -60px;
  width: 300px;
  height: 300px;
  border: 2px solid rgba(64, 192, 160, 0.15);
  border-radius: 50%;
  pointer-events: none;
}

.login-left::before {
  content: '';
  position: absolute;
  bottom: -100px;
  right: 100px;
  width: 200px;
  height: 200px;
  border: 2px solid rgba(64, 192, 160, 0.1);
  border-radius: 30px;
  transform: rotate(45deg);
  pointer-events: none;
}

.left-content {
  max-width: 520px;
  position: relative;
  z-index: 1;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 3rem;
}

.brand-icon {
  width: 40px;
  height: 40px;
  background: #40c0a0;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0d1b2a;
}

.brand-name {
  font-size: 1rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.tagline {
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 1rem;
  color: #ffffff;
}

.tagline-sub {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.6);
  margin: 0 0 2.5rem;
}

.features {
  list-style: none;
  padding: 0;
  margin: 0 0 3rem;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.feature-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(64, 192, 160, 0.15);
  color: #40c0a0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
}

.feature-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.feature-text strong {
  color: #ffffff;
  font-size: 0.95rem;
}

.feature-text span {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
  line-height: 1.4;
}

.footer-note {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.3);
  margin: 0;
}

/* === Right panel — login form === */
.login-right {
  flex: 1;
  background: #f0f2f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
}

.login-card h2 {
  margin: 0 0 0.5rem;
  color: #1a1a1a;
  font-size: 1.4rem;
  font-weight: 700;
}

.login-card .subtitle {
  text-align: left;
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #333;
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  pointer-events: none;
}

input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #40c0a0;
  box-shadow: 0 0 0 3px rgba(64, 192, 160, 0.15);
}

.login-btn {
  width: 100%;
  padding: 0.85rem;
  background: linear-gradient(135deg, #1a7a6d 0%, #2a9d8f 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.login-btn:hover:not(:disabled) {
  opacity: 0.9;
}

.login-btn:active:not(:disabled) {
  transform: scale(0.98);
}

.login-btn:disabled {
  background: #a0d8c0;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: center;
  background: #fef2f2;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #fecaca;
}

.info-note {
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.info-note svg {
  flex-shrink: 0;
  color: #6c757d;
  margin-top: 2px;
}

.info-note p {
  margin: 0;
  font-size: 0.82rem;
  color: #6c757d;
  line-height: 1.5;
}

.admin-link {
  margin-top: 2rem;
  font-size: 0.85rem;
  color: #999;
}

.admin-link a {
  color: #1a7a6d;
  text-decoration: none;
  font-weight: 500;
}

.admin-link a:hover {
  text-decoration: underline;
}

/* === Responsive === */
@media (max-width: 900px) {
  .login-page {
    flex-direction: column;
  }

  .login-left {
    padding: 2rem;
    min-height: auto;
  }

  .tagline {
    font-size: 1.6rem;
  }

  .features {
    display: none;
  }

  .login-right {
    padding: 1.5rem;
  }
}
</style>