<template>
  <div class="my-access-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Мої доступи</h1>
        <p class="page-subtitle">Сервіси, до яких адміністратор надав вам доступ</p>
      </div>
    </div>

    <!-- Filter Block -->
    <div class="filter-block">
      <div class="filter-search">
        <svg class="filter-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 21L16.6569 16.6569M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <input
          type="text"
          v-model="store.searchQuery"
          placeholder="Пошук за сервісом, логином або адресою..."
          class="filter-input"
        />
      </div>

      <div class="filter-select-wrapper">
        <select
          v-model="filterService"
          class="filter-select"
        >
          <option value="">Усі джерела</option>
          <option
            v-for="svc in store.services"
            :key="svc.service_id"
            :value="svc.service_id"
          >
            {{ svc.service_name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Services List -->
    <div class="services-grid">
      <div v-if="store.loading" class="loading-state">
        <div class="spinner"></div>
        <p>Завантаження...</p>
      </div>

      <div v-else-if="filteredServices.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C20.1046 9 21 8.10457 21 7V5C21 3.89543 20.1046 3 19 3H5C3.89543 3 3 3.89543 3 5V7C3 8.10457 3.89543 9 5 9V11M19 11H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p>Доступи не знайдено</p>
        <p class="empty-hint">Зверніться до адміністратора для надання доступу</p>
      </div>

      <div
        v-else
        v-for="(service, sIndex) in paginatedServices"
        :key="service.service_id"
        class="service-card"
      >
        <!-- Service Header -->
        <div class="service-header">
          <div class="service-icon" :style="{ backgroundColor: getServiceColor(sIndex) }">
            <img
              v-if="service.service_logo_url"
              :src="service.service_logo_url"
              :alt="service.service_name"
              class="service-avatar"
              @error="(e) => handleAvatarError(e, service)"
            />
            <span v-if="!service.service_logo_url || avatarErrors.has(service.service_id)" class="icon-letter">{{ getInitials(service.service_name) }}</span>
          </div>
          <div class="service-info">
            <h3 class="service-name">{{ service.service_name }}</h3>
            <a
              v-if="service.service_url"
              :href="service.service_url"
              target="_blank"
              rel="noopener noreferrer"
              class="service-url"
            >
              {{ service.service_url }}
            </a>
            <p v-else class="service-url">—</p>
          </div>
        </div>

        <!-- Credentials List -->
        <div class="credentials-list">
          <div
            v-for="cred in service.credentials"
            :key="cred.credential_id"
            class="credential-row"
          >
            <div class="credential-field">
              <label class="field-label">Логін</label>
              <div class="field-value-wrapper">
                <span class="field-value">{{ cred.login || '—' }}</span>
                <button class="btn-icon btn-copy" @click="copyToClipboard(cred.login || '')" title="Копіювати">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 4V16C8 17.1046 8.89543 18 10 18H18C19.1046 18 20 17.1046 20 16V4C20 2.89543 19.1046 2 18 2H10C8.89543 2 8 2.89543 8 4ZM16 18V20C16 21.1046 15.1046 22 14 22H4C2.89543 22 2 21.1046 2 20V8C2 6.89543 2.89543 6 4 6H10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>

            <div class="credential-field">
              <label class="field-label">Пароль</label>
              <div class="field-value-wrapper">
                <span v-if="passwordVisibility.has(cred.credential_id)" class="field-value password-value">{{ cred.protected_password || '—' }}</span>
                <span v-else class="field-value password-dots">••••••••••</span>
                <button class="btn-icon btn-eye" @click="togglePassword(cred.credential_id)" :title="passwordVisibility.has(cred.credential_id) ? 'Сховати' : 'Показати'">
                  <svg v-if="!passwordVisibility.has(cred.credential_id)" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="btn-icon btn-copy" @click="copyToClipboard(cred.protected_password || '')" title="Копіювати">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 4V16C8 17.1046 8.89543 18 10 18H18C19.1046 18 20 17.1046 20 16V4C20 2.89543 19.1046 2 18 2H10C8.89543 2 8 2.89543 8 4ZM16 18V20C16 21.1046 15.1046 22 14 22H4C2.89543 22 2 21.1046 2 20V8C2 6.89543 2.89543 6 4 6H10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="filteredServices.length > 0" class="pagination">
      <button
        class="btn-pagination"
        :disabled="currentPage === 1"
        @click="currentPage = 1"
        title="Перша сторінка"
      >
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11 17L6 12L11 7M18 17L13 12L18 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <button
        class="btn-pagination"
        :disabled="currentPage === 1"
        @click="currentPage--"
        title="Попередня сторінка"
      >
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <span class="pagination-info">{{ paginationStart }}-{{ paginationEnd }} з {{ filteredServices.length }}</span>
      <button
        class="btn-pagination"
        :disabled="currentPage === totalPages"
        @click="currentPage++"
        title="Наступна сторінка"
      >
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <button
        class="btn-pagination"
        :disabled="currentPage === totalPages"
        @click="currentPage = totalPages"
        title="Остання сторінка"
      >
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M13 17L18 12L13 7M6 17L11 12L6 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>

    <!-- Toast notification -->
    <div v-if="toastMessage" class="toast">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useMyAccessStore } from '@/stores/myAccess'

const router = useRouter()
const store = useMyAccessStore()
const filterService = ref<number | ''>('')
const passwordVisibility = ref(new Set<number>())
const avatarErrors = ref(new Set<number>())
const toastMessage = ref('')
let toastTimer: ReturnType<typeof setTimeout> | null = null

const filteredServices = computed(() => {
  let result = store.filteredServices
  if (filterService.value !== '') {
    result = result.filter(s => s.service_id === filterService.value)
  }
  return result
})

const currentPage = ref(1)
const pageSize = 10

const totalPages = computed(() => Math.ceil(filteredServices.value.length / pageSize))

const paginatedServices = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredServices.value.slice(start, start + pageSize)
})

const paginationStart = computed(() => {
  if (filteredServices.value.length === 0) return 0
  return (currentPage.value - 1) * pageSize + 1
})

const paginationEnd = computed(() => {
  const end = currentPage.value * pageSize
  return end > filteredServices.value.length ? filteredServices.value.length : end
})

watch(filteredServices, () => {
  currentPage.value = 1
})

const serviceColors = [
  '#5865F2', '#EA4335', '#0052CC', '#333', '#FF6600',
  '#0078D4', '#4285F4', '#1DA1F2', '#000', '#7B68EE'
]

function getServiceColor(index: number): string {
  return serviceColors[index % serviceColors.length] || '#5865F2'
}

function getInitials(name: string | undefined): string {
  return (name || '?').charAt(0).toUpperCase()
}

function handleAvatarError(event: Event, service: any) {
  avatarErrors.value.add(service.service_id)
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}

function navigateToDetail(service: any) {
  router.push(`/service/${service.service_id}`)
}

function togglePassword(credentialId: number) {
  const visible = new Set(passwordVisibility.value)
  if (visible.has(credentialId)) {
    visible.delete(credentialId)
  } else {
    visible.add(credentialId)
  }
  passwordVisibility.value = visible
}

function copyToClipboard(text: string) {
  if (!text) return
  navigator.clipboard.writeText(text).then(() => {
    showToast('Скопійовано в буфер обміну')
  })
}

function showToast(message: string) {
  toastMessage.value = message
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2000)
}

onMounted(() => {
  store.fetchMyAccess()
})
</script>

<style scoped>
.my-access-page {
  width: 100%;
  padding-bottom: 2rem;
}

/* Page Header */
.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.25rem 0;
}

.page-subtitle {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

/* Filter Block */
.filter-block {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-search {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.filter-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.125rem;
  height: 1.125rem;
  color: #94a3b8;
  pointer-events: none;
}

.filter-input {
  width: 100%;
  padding: 0.625rem 1rem 0.625rem 2.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  color: #0f172a;
  background: #f8fafc;
  outline: none;
  transition: all 0.2s;
}

.filter-input:focus {
  border-color: #5865F2;
  background: white;
  box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.1);
}

.filter-select-wrapper {
  position: relative;
}

.filter-select {
  appearance: none;
  padding: 0.625rem 2.5rem 0.625rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  color: #0f172a;
  background: #f8fafc;
  cursor: pointer;
  outline: none;
  transition: all 0.2s;
  min-width: 160px;
}

.filter-select:focus {
  border-color: #5865F2;
  background: white;
  box-shadow: 0 0 0 3px rgba(88, 101, 242, 0.1);
}

.filter-select-wrapper::after {
  content: '';
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px solid #64748b;
  pointer-events: none;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.25rem;
}

/* Service Card */
.service-card {
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow: hidden;
  transition: all 0.2s;
}

.service-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

/* Service Header */
.service-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.service-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.service-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.75rem;
}

.icon-letter {
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
}

.service-info {
  flex: 1;
  min-width: 0;
}

.service-name {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.service-url {
  font-size: 0.75rem;
  color: #3b82f6;
  margin: 0.125rem 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-decoration: none;
  cursor: pointer;
  display: block;
}

.service-url:hover {
  color: #2563eb;
  text-decoration: underline;
}

/* Credentials List */
.credentials-list {
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.credential-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.credential-field {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.field-label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-value-wrapper {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 0.375rem 0.5rem;
}

.field-value {
  flex: 1;
  font-size: 0.8125rem;
  color: #0f172a;
  font-family: 'Courier New', monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.password-dots {
  letter-spacing: 0.1em;
}

/* Icon Buttons */
.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 0.375rem;
  color: #94a3b8;
  transition: all 0.2s;
  flex-shrink: 0;
}

.btn-icon:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-icon svg {
  width: 16px;
  height: 16px;
}

/* Service Footer */
.service-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid #f1f5f9;
}

.btn-view-service {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-view-service:hover {
  background: #f1f5f9;
  color: #0f172a;
  border-color: #cbd5e1;
}

.btn-view-service svg {
  width: 16px;
  height: 16px;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #94a3b8;
}

.spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid #e2e8f0;
  border-top-color: #5865F2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state svg {
  width: 4rem;
  height: 4rem;
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1rem;
  margin: 0 0 0.25rem 0;
  color: #64748b;
}

.empty-hint {
  font-size: 0.8125rem !important;
  color: #94a3b8 !important;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: #0f172a;
  color: white;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(1rem);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.5rem 0 1rem;
}

.btn-pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pagination:hover:not(:disabled) {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #0f172a;
}

.btn-pagination:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-pagination svg {
  width: 18px;
  height: 18px;
}

.pagination-info {
  font-size: 0.875rem;
  color: #64748b;
  padding: 0 0.75rem;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .services-grid {
    grid-template-columns: 1fr;
  }

  .filter-block {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-search {
    min-width: 100%;
  }

  .filter-select {
    width: 100%;
  }
}
</style>
