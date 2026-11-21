<template>
  <div class="sources-page">
    <!-- Dashboard -->
    <div class="dashboard-stats">
      <div class="stat-card">
        <div class="stat-icon passwords">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 15V17M12 11H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ servicesStore.totalPasswords }}</div>
          <div class="stat-label">Кількість паролів</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon sources">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C20.1046 9 21 8.10457 21 7V5C21 3.89543 20.1046 3 19 3H5C3.89543 3 3 3.89543 3 5V7C3 8.10457 3.89543 9 5 9V11M19 11H5M12 15V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ servicesStore.totalSources }}</div>
          <div class="stat-label">Кількість джерел</div>
        </div>
      </div>
    </div>

    <!-- Filter Block -->
    <div class="filter-block">
      <div class="filter-row">
        <div class="filter-search">
          <svg class="filter-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 21L16.6569 16.6569M19 11C19 15.4183 15.4183 19 11 19C6.58172 19 3 15.4183 3 11C3 6.58172 6.58172 3 11 3C15.4183 3 19 6.58172 19 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <input
            type="text"
            v-model="servicesStore.searchQuery"
            placeholder="Пошук за всіма полями..."
            class="filter-input"
          />
        </div>

        <div class="filter-select-wrapper">
          <select
            v-model="servicesStore.filterSource"
            class="filter-select"
          >
            <option value="">Усі джерела</option>
            <option
              v-for="source in servicesStore.uniqueSourceNames"
              :key="source.id"
              :value="source.id"
            >
              {{ source.name }}
            </option>
          </select>
        </div>

        <button class="btn btn-secondary" @click="resetFilters">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 10C3 6.41015 5.61766 3 9 3C12.3823 3 15 6.41015 15 10C15 13.5899 12.3823 17 9 17C6.62604 17 4.54687 15.6979 3.61807 13.7819" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M3 3V10H10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Скинути фільтр
        </button>

        <button v-if="isAdmin" class="btn btn-primary" @click="openAddDialog">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Додати джерело
        </button>
      </div>
    </div>

    <!-- Sources List -->
    <div class="sources-list">
      <div v-if="servicesStore.loading" class="loading-state">
        <div class="spinner"></div>
        <p>Завантаження...</p>
      </div>

      <div v-else-if="servicesStore.filteredServices.length === 0" class="empty-state">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C20.1046 9 21 8.10457 21 7V5C21 3.89543 20.1046 3 19 3H5C3.89543 3 3 3.89543 3 5V7C3 8.10457 3.89543 9 5 9V11M19 11H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p>Джерела не знайдено</p>
      </div>

      <div
        v-else
        v-for="service in servicesStore.filteredServices"
        :key="service.service_id"
        class="source-card"
        @click="openEditDialog(service)"
      >
        <div class="source-logo" @click.stop>
          <img
            v-if="service.service_logo_url"
            :src="service.service_logo_url"
            :alt="service.service_name"
            @error="(e: Event) => { (e.target as HTMLImageElement).style.display = 'none' }"
          />
          <div v-else class="logo-placeholder">
            {{ getInitials(service.service_name) }}
          </div>
        </div>

        <div class="source-info">
          <div class="source-name">{{ service.service_name }}</div>
          <div class="source-passwords">{{ service.credential_count }} паролів</div>
        </div>

        <div class="source-actions">
          <button class="btn btn-sm btn-add-password" @click.stop="openAddPasswordDialog(service)">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Згенерувати пароль
          </button>

          <button v-if="isAdmin" class="btn btn-sm btn-delete" @click.stop="confirmDelete(service)">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Видалити
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Dialog -->
    <div v-if="showDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <h3>{{ editingService ? 'Редагувати джерело' : 'Додати джерело' }}</h3>
          <button class="dialog-close" @click="closeDialog">&times;</button>
        </div>

        <form @submit.prevent="saveService" class="dialog-form">
          <div class="form-group">
            <label for="service-name">Назва джерела *</label>
            <input
              id="service-name"
              v-model="formData.service_name"
              type="text"
              required
              placeholder="Наприклад: Gmail"
            />
          </div>

          <div class="form-group">
            <label for="service-url">URL</label>
            <input
              id="service-url"
              v-model="formData.service_url"
              type="url"
              placeholder="https://mail.google.com"
            />
          </div>

          <div class="form-group">
            <label for="service-logo">URL логотипу</label>
            <input
              id="service-logo"
              v-model="formData.service_logo_url"
              type="url"
              placeholder="https://example.com/logo.png"
            />
          </div>

          <div class="dialog-actions">
            <button type="button" class="btn btn-secondary" @click="closeDialog">Скасувати</button>
            <button type="submit" class="btn btn-primary">{{ editingService ? 'Зберегти' : 'Додати' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <div v-if="showDeleteDialog" class="dialog-overlay" @click="showDeleteDialog = false">
      <div class="dialog delete-dialog" @click.stop>
        <div class="dialog-header">
          <h3>Підтвердження видалення</h3>
          <button class="dialog-close" @click="showDeleteDialog = false">&times;</button>
        </div>
        <p class="delete-message">Ви впевнені, що хочете видалити джерело "{{ deleteTarget?.service_name }}"? Усі паролі цього джерела також будуть видалені.</p>
        <div class="dialog-actions">
          <button class="btn btn-secondary" @click="showDeleteDialog = false">Скасувати</button>
          <button class="btn btn-danger" @click="deleteConfirmed">Видалити</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useServicesStore } from '@/stores/services'

const authStore = useAuthStore()
const servicesStore = useServicesStore()

const isAdmin = computed(() => authStore.user?.role === 'admin')

// Dialog state
const showDialog = ref(false)
const showDeleteDialog = ref(false)
const editingService = ref<{ service_id: number; service_name: string; service_url: string | null; service_logo_url: string | null } | null>(null)
const deleteTarget = ref<{ service_id: number; service_name: string } | null>(null)

const formData = ref({
  service_name: '',
  service_url: '',
  service_logo_url: '',
})

function getInitials(name: string) {
  return name.charAt(0).toUpperCase()
}

function resetFilters() {
  servicesStore.searchQuery = ''
  servicesStore.filterSource = ''
}

function openAddDialog() {
  editingService.value = null
  formData.value = { service_name: '', service_url: '', service_logo_url: '' }
  showDialog.value = true
}

function openEditDialog(service: { service_id: number; service_name: string; service_url: string | null; service_logo_url: string | null }) {
  editingService.value = service
  formData.value = {
    service_name: service.service_name,
    service_url: service.service_url || '',
    service_logo_url: service.service_logo_url || '',
  }
  showDialog.value = true
}

function closeDialog() {
  showDialog.value = false
  editingService.value = null
}

function openAddPasswordDialog(service: { service_name: string }) {
  // TODO: реалізувати додавання пароля
  console.log('Додати пароль для:', service.service_name)
}

function confirmDelete(service: { service_id: number; service_name: string }) {
  deleteTarget.value = service
  showDeleteDialog.value = true
}

async function saveService() {
  if (editingService.value) {
    await servicesStore.updateService(editingService.value.service_id, formData.value)
  } else {
    await servicesStore.createService(formData.value)
  }
  closeDialog()
}

async function deleteConfirmed() {
  if (deleteTarget.value) {
    await servicesStore.deleteService(deleteTarget.value.service_id)
  }
  showDeleteDialog.value = false
  deleteTarget.value = null
}

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchProfile()
  }
  servicesStore.fetchServices()
})
</script>

<style scoped>
.sources-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Dashboard Stats */
.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon.passwords {
  background: #dbeafe;
  color: #2563eb;
}

.stat-icon.sources {
  background: #dcfce7;
  color: #16a34a;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Filter Block */
.filter-block {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem;
}

.filter-row {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-search {
  position: relative;
  flex: 1;
  min-width: 200px;
}

.filter-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.filter-input {
  width: 100%;
  padding: 0.625rem 0.75rem 0.625rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.filter-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.filter-select {
  padding: 0.625rem 2rem 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  background-color: white;
  cursor: pointer;
  min-width: 150px;
  transition: border-color 0.2s;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.filter-select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid transparent;
  white-space: nowrap;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: white;
  color: #475569;
  border-color: #e2e8f0;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
}

.btn-sm svg {
  width: 14px;
  height: 14px;
}

.btn-add-password {
  background: #dcfce7;
  color: #16a34a;
  border-color: #bbf7d0;
}

.btn-add-password:hover {
  background: #bbf7d0;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.btn-delete:hover {
  background: #fee2e2;
}

/* Sources List */
.sources-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.source-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.source-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.source-logo {
  width: 48px;
  height: 48px;
  border-radius: 0.75rem;
  overflow: hidden;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
}

.source-logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-placeholder {
  font-size: 1.25rem;
  font-weight: 700;
  color: #64748b;
}

.source-info {
  flex: 1;
  min-width: 0;
}

.source-name {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.source-passwords {
  font-size: 0.875rem;
  color: #64748b;
  margin-top: 0.125rem;
}

.source-actions {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #94a3b8;
  gap: 1rem;
}

.loading-state svg,
.empty-state svg {
  width: 48px;
  height: 48px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Dialog */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.dialog {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 480px;
  padding: 1.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.dialog-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #0f172a;
}

.dialog-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.25rem;
  line-height: 1;
}

.dialog-close:hover {
  color: #475569;
}

.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  padding: 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.dialog-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.delete-message {
  color: #475569;
  font-size: 0.9375rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

/* Responsive */
@media (max-width: 640px) {
  .filter-row {
    flex-direction: column;
  }

  .filter-search {
    width: 100%;
  }

  .filter-select {
    width: 100%;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .source-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .source-actions {
    width: 100%;
    justify-content: flex-end;
  }
}
</style>
