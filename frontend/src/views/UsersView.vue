<template>
  <div class="users-view">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1>Працівники</h1>
        <p class="page-subtitle">Керуйте обліковими записами, доступами та блокуванням</p>
      </div>
    </div>

    <!-- Dashboard Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon blue">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M17 21V19C17 18.4696 16.7893 17.9609 16.4142 17.5858C16.0391 17.2107 15.5304 17 15 17H9C8.46957 17 7.96086 17.2107 7.58579 17.5858C7.21071 17.9609 7 18.4696 7 19V21M9 11C10.6569 11 12 9.65685 12 8C12 6.34315 10.6569 5 9 5C7.34315 5 6 6.34315 6 8C6 9.65685 7.34315 11 9 11ZM14 7C15.6569 7 17 5.65685 17 4C17 2.34315 15.6569 1 14 1C12.3431 1 11 2.34315 11 4C11 5.65685 12.3431 7 14 7ZM20 19V21M20 17C19.4696 17 18.9609 17.2107 18.5858 17.5858C18.2107 17.9609 18 18.4696 18 19V21M14 11C15.6569 11 17 12.3431 17 14C17 14.5304 16.7893 15.0391 16.4142 15.4142C16.0391 15.7893 15.5304 16 15 16H9C8.46957 16 7.96086 15.7893 7.58579 15.4142C7.21071 15.0391 7 14.5304 7 14C7 12.3431 8.34315 11 10 11H14Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ store.totalCount }}</span>
          <span class="stat-label">Усього працівників</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon green">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M12 11C13.6569 11 15 9.65685 15 8C15 6.34315 13.6569 5 12 5C10.3431 5 9 6.34315 9 8C9 9.65685 10.3431 11 12 11ZM21 21V19C20.9993 18.1597 20.7047 17.3512 20.1614 16.7175C19.6182 16.0837 18.8671 15.6634 18.0501 15.5393C18.0338 15.2246 18.0114 14.9111 17.9831 14.5989C17.9479 14.2085 17.9064 13.8192 17.8586 13.4311C17.6234 12.4421 17.0853 11.5525 16.3245 10.9005C15.5636 10.2485 14.6181 9.87337 13.6316 9.84002C13.1892 8.8297 12.502 7.97258 11.6442 7.36306C10.7864 6.75354 9.78348 6.41522 8.74999 6.37649C8.33001 6.37649 7.91003 6.41522 7.49005 6.49265C6.50356 6.54044 5.55804 6.91557 4.79718 7.56756C4.03632 8.21955 3.4982 9.10917 3.26299 10.0982C3.2152 10.4863 3.17373 10.8756 3.13853 11.266C3.11022 11.5781 3.08784 11.8916 3.07155 12.2063" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ store.activeCount }}</span>
          <span class="stat-label">Активні</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon red">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.364 18.364L5.63605 5.63604M18.364 5.63604L5.63605 18.364" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
          </svg>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ store.blockedCount }}</span>
          <span class="stat-label">Заблоковані</span>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="search-input-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="currentColor" stroke-width="2"/>
          <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input
          v-model="store.searchQuery"
          type="text"
          class="search-input"
          placeholder="Пошук за іменем, логіном, телефоном..."
        />
      </div>

      <select v-model="store.statusFilter" class="status-select">
        <option value="">Усі статуси</option>
        <option value="active">Активні</option>
        <option value="blocked">Заблоковані</option>
      </select>

      <button class="btn btn-add" @click="openAddDialog">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Додати працівника
      </button>
    </div>

    <!-- Employees Table -->
    <div class="table-card">
      <div class="table-header">
        <span class="col-employee">ПРАЦІВНИК</span>
        <span class="col-phone">ТЕЛЕФОН</span>
        <span class="col-accesses">ДОСТУПИ</span>
        <span class="col-status">СТАТУС</span>
        <span class="col-actions"></span>
      </div>

      <div v-if="store.filteredEmployees.length === 0" class="empty-state">
        <p>Працівників не знайдено</p>
      </div>

      <div v-for="emp in store.filteredEmployees" :key="emp.user_id" class="table-row" @click="goToEmployee(emp.user_id)">
        <div class="col-employee">
          <div class="employee-avatar" :style="{ backgroundColor: getAvatarColor(emp.full_name || emp.login || '?') }">
            {{ getInitials(emp.full_name || emp.login || '?') }}
          </div>
          <div class="employee-info">
            <span class="employee-name">{{ emp.full_name }}</span>
            <span class="employee-login">{{ emp.login }}</span>
          </div>
        </div>
        <div class="col-phone">{{ emp.phone || '—' }}</div>
        <div class="col-accesses">
          <span class="access-count">{{ emp.access_count }} {{ getServiceWord(emp.access_count) }}</span>
        </div>
        <div class="col-status">
          <span :class="['status-badge', emp.status === 'active' ? 'status-active' : 'status-blocked']">
            {{ emp.status === 'active' ? 'Активний' : 'Заблокований' }}
          </span>
        </div>
        <div class="col-actions">
          <button class="btn-icon btn-accesses" title="Доступи" @click.stop="openAccessModal(emp)">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
              <path d="M12 12C13.1046 12 14 11.1046 14 10C14 8.89543 13.1046 8 12 8C10.8954 8 10 8.89543 10 10C10 11.1046 10.8954 12 12 12Z" stroke="currentColor" stroke-width="2"/>
            </svg>
            Доступи
          </button>
          <button
            :class="['btn-icon', emp.status === 'active' ? 'btn-block' : 'btn-unblock']"
            :title="emp.status === 'active' ? 'Заблокувати' : 'Розблокувати'"
            @click.stop="toggleStatus(emp)"
          >
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18.364 18.364L5.63605 5.63604M18.364 5.63604L5.63605 18.364" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
          <button class="btn-icon btn-delete" title="Видалити" @click.stop="confirmDelete(emp)">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Add Employee Dialog -->
    <Teleport to="body">
      <div v-if="showAddDialog" class="modal-overlay" @click.self="closeAddDialog">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3>Додати працівника</h3>
            <button class="btn-close" @click="closeAddDialog">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>ПІБ</label>
              <input v-model="addForm.full_name" type="text" placeholder="Введіть повне ім'я" />
            </div>
            <div class="form-group">
              <label>Логін</label>
              <input v-model="addForm.login" type="text" placeholder="Введіть логін" />
            </div>
            <div class="form-group">
              <label>Пароль</label>
              <div class="password-input-wrapper">
                <input :type="addPasswordVisible ? 'text' : 'password'" v-model="addForm.password" placeholder="Введіть пароль" />
                <button type="button" class="btn-password-toggle" @click="addPasswordVisible = !addPasswordVisible">
                  <svg v-if="!addPasswordVisible" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 12C13.1046 12 14 11.1046 14 10C14 8.89543 13.1046 8 12 8C10.8954 8 10 8.89543 10 10C10 11.1046 10.8954 12 12 12Z" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.94 17.94A10.07 10.07 0 013 12C3 12 7 4 12 4C14.53 4 16.95 5.02 18.94 6.58M1 1L23 23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
            </div>
            <div class="form-group">
              <label>Телефон</label>
              <input v-model="addForm.phone" type="text" placeholder="+380 XX XXX XX XX" />
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeAddDialog">Скасувати</button>
            <button class="btn btn-primary" @click="handleAddEmployee">Зберегти</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation Dialog -->
    <Teleport to="body">
      <div v-if="showDeleteDialog" class="modal-overlay" @click.self="closeDeleteDialog">
        <div class="modal-dialog modal-small">
          <div class="modal-header">
            <h3>Видалити працівника?</h3>
            <button class="btn-close" @click="closeDeleteDialog">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <p>Ви дійсно хочете видалити <strong>{{ deleteTarget?.full_name }}</strong>?</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeDeleteDialog">Скасувати</button>
            <button class="btn btn-danger" @click="handleDelete">Видалити</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Access Modal -->
    <Teleport to="body">
      <div v-if="showAccessModal" class="modal-overlay" @click.self="closeAccessModal">
        <div class="modal-dialog modal-access">
          <div class="modal-header">
            <h3>Доступи: {{ accessTarget?.full_name }}</h3>
            <button class="btn-close" @click="closeAccessModal">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="detailStore.credentials.length === 0" class="empty-state">
              <p>Доступів ще не надано</p>
            </div>
            <div v-for="cred in detailStore.credentials" :key="cred.credential_id" class="access-item">
              <div class="access-service-icon" :style="{ backgroundColor: getServiceColor(cred.service_name) }">
                <img
                  v-if="cred.service_logo_url"
                  :src="cred.service_logo_url"
                  :alt="cred.service_name"
                  class="access-logo"
                  @error="handleAccessLogoError($event, cred)"
                />
                <span v-else class="access-letter">{{ cred.service_name.charAt(0).toUpperCase() }}</span>
              </div>
              <div class="access-item-info">
                <span class="access-service-name">{{ cred.service_name }}</span>
                <span class="access-login-value">{{ cred.login }}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeAccessModal">Закрити</button>
            <button class="btn btn-primary" @click="goToEmployeeFromModal">До деталей</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useEmployeesStore } from '@/stores/employees'
import { useEmployeeDetailStore } from '@/stores/employeeDetail'

const router = useRouter()
const store = useEmployeesStore()
const detailStore = useEmployeeDetailStore()

const avatarColors = [
  '#059669', '#2563eb', '#d97706', '#7c3aed', '#dc2626',
  '#0891b2', '#4f46e5', '#c026d3', '#ea580c', '#16a34a'
]

function getAvatarColor(name: string): string {
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return avatarColors[Math.abs(hash) % avatarColors.length] ?? '#059669'
}

function getInitials(name: string): string {
  return name.charAt(0).toUpperCase()
}

function goToEmployee(user_id: number) {
  router.push(`/employee/${user_id}`)
}

function goToEmployeeFromModal() {
  if (!accessTarget.value) return
  const userId = accessTarget.value.user_id
  closeAccessModal()
  router.push(`/employee/${userId}`)
}

function handleAccessLogoError(event: Event, cred: any) {
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  const letterSpan = img.nextElementSibling as HTMLSpanElement
  if (letterSpan) letterSpan.style.display = 'inline'
}

const serviceColors = [
  '#5865F2', '#EA4335', '#0078D4', '#181717', '#FF9900',
  '#00A4EF', '#4265B5', '#00B4E6', '#FF6C37', '#000000'
]

function getServiceColor(name: string): string {
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return serviceColors[Math.abs(hash) % serviceColors.length] ?? '#5865F2'
}

// Access modal
const showAccessModal = ref(false)
const accessTarget = ref<{ user_id: number; full_name: string | null } | null>(null)

async function openAccessModal(emp: { user_id: number; full_name: string | null }) {
  accessTarget.value = emp
  showAccessModal.value = true
  await detailStore.fetchCredentials(emp.user_id)
}

function closeAccessModal() {
  showAccessModal.value = false
  accessTarget.value = null
}

function getServiceWord(count: number): string {
  if (count % 10 === 1 && count % 100 !== 11) return 'сервіс'
  if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) return 'сервіси'
  return 'сервісів'
}

// Add dialog
const showAddDialog = ref(false)
const addPasswordVisible = ref(false)
const addForm = ref({
  full_name: '',
  login: '',
  password: '',
  phone: ''
})

function openAddDialog() {
  showAddDialog.value = true
  addForm.value = { full_name: '', login: '', password: '', phone: '' }
  addPasswordVisible.value = false
}

function closeAddDialog() {
  showAddDialog.value = false
}

async function handleAddEmployee() {
  if (!addForm.value.full_name || !addForm.value.login || !addForm.value.password) return
  const result = await store.createEmployee(addForm.value)
  if (result) {
    closeAddDialog()
  }
}

// Delete dialog
const showDeleteDialog = ref(false)
const deleteTarget = ref<{ user_id: number; full_name: string | null } | null>(null)

function confirmDelete(emp: { user_id: number; full_name: string | null }) {
  deleteTarget.value = emp
  showDeleteDialog.value = true
}

function closeDeleteDialog() {
  showDeleteDialog.value = false
  deleteTarget.value = null
}

async function handleDelete() {
  if (!deleteTarget.value) return
  await store.deleteEmployee(deleteTarget.value.user_id)
  closeDeleteDialog()
}

// Toggle status
async function toggleStatus(emp: { user_id: number; status: string | null }) {
  const newStatus = emp.status === 'active' ? 'blocked' : 'active'
  await store.updateStatus(emp.user_id, newStatus)
}

onMounted(() => {
  store.fetchEmployees()
})
</script>

<style scoped>
.users-view {
  width: 100%;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #0f172a;
}

.page-subtitle {
  margin: 0.25rem 0 0;
  font-size: 0.875rem;
  color: #64748b;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: #fff;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
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

.stat-icon.blue {
  background: #eff6ff;
  color: #2563eb;
}

.stat-icon.green {
  background: #f0fdf4;
  color: #16a34a;
}

.stat-icon.red {
  background: #fef2f2;
  color: #dc2626;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.25rem;
}

/* Filter Bar */
.filter-bar {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  align-items: center;
}

.search-input-wrapper {
  flex: 1;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.625rem 0.75rem 0.625rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.15s;
}

.search-input:focus {
  border-color: #2563eb;
}

.status-select {
  padding: 0.625rem 2rem 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: #fff;
  outline: none;
  cursor: pointer;
  min-width: 160px;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  background: #0d9488;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.15s;
}

.btn-add:hover {
  background: #0f766e;
}

.btn-add svg {
  width: 16px;
  height: 16px;
}

/* Table */
.table-card {
  background: #fff;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1fr 1fr auto;
  padding: 0.75rem 1.25rem;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.7rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  align-items: center;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1.2fr 1fr 1fr auto;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  align-items: center;
  transition: background-color 0.15s;
  cursor: pointer;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: #f8fafc;
}

.col-employee {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.employee-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 0.875rem;
  flex-shrink: 0;
}

.employee-info {
  display: flex;
  flex-direction: column;
}

.employee-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: #0f172a;
}

.employee-login {
  font-size: 0.75rem;
  color: #94a3b8;
}

.col-phone {
  font-size: 0.875rem;
  color: #475569;
}

.col-accesses {
  font-size: 0.875rem;
  color: #475569;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #dcfce7;
  color: #166534;
}

.status-blocked {
  background: #fee2e2;
  color: #991b1b;
}

.col-actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #fff;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.btn-icon svg {
  width: 16px;
  height: 16px;
}

.btn-accesses {
  color: #475569;
}

.btn-accesses:hover {
  background: #f1f5f9;
}

.btn-block {
  color: #dc2626;
  border-color: #fecaca;
  background: #fef2f2;
}

.btn-block:hover {
  background: #fee2e2;
}

.btn-unblock {
  color: #16a34a;
  border-color: #bbf7d0;
  background: #f0fdf4;
}

.btn-unblock:hover {
  background: #dcfce7;
}

.btn-delete {
  color: #dc2626;
  border-color: #fecaca;
  background: #fef2f2;
  padding: 0.375rem;
}

.btn-delete:hover {
  background: #fee2e2;
}

.empty-state {
  padding: 3rem;
  text-align: center;
  color: #94a3b8;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-dialog {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.modal-small {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.125rem;
  color: #0f172a;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
}

.btn-close svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  margin-bottom: 1.25rem;
}

.modal-body p {
  margin: 0;
  color: #475569;
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-size: 0.8rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.375rem;
}

.form-group input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #2563eb;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper input {
  padding-right: 2.5rem;
}

.btn-password-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
}

.btn-password-toggle svg {
  width: 18px;
  height: 18px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.btn-primary {
  padding: 0.625rem 1.5rem;
  background: #0d9488;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s;
}

.btn-primary:hover {
  background: #0f766e;
}

.btn-secondary {
  padding: 0.625rem 1.5rem;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-danger {
  padding: 0.625rem 1.5rem;
  background: #dc2626;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s;
}

.btn-danger:hover {
  background: #b91c1c;
}

/* Access Modal */
.modal-access {
  max-width: 500px;
}

.access-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}

.access-item:last-child {
  margin-bottom: 0;
}

.access-service-icon {
  width: 36px;
  height: 36px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.access-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}

.access-letter {
  color: #fff;
  font-weight: 600;
  font-size: 0.875rem;
}

.access-item-info {
  display: flex;
  flex-direction: column;
}

.access-service-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: #0f172a;
}

.access-login-value {
  font-size: 0.75rem;
  color: #94a3b8;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .status-select {
    width: 100%;
  }

  .btn-add {
    width: 100%;
    justify-content: center;
  }

  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr auto;
  }

  .col-phone,
  .col-accesses,
  .col-status {
    display: none;
  }
}
</style>
