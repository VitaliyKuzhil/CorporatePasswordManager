<template>
  <div class="employee-detail-view">
    <!-- Back Button -->
    <button class="btn-back" @click="$router.push('/users')">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      До списку працівників
    </button>

    <!-- Employee Info Card -->
    <div class="employee-card" v-if="store.employee">
      <div class="employee-avatar-large" :style="{ backgroundColor: getAvatarColor(store.employee.full_name || store.employee.login || '?') }">
        {{ getInitials(store.employee.full_name || store.employee.login || '?') }}
      </div>
      <div class="employee-details">
        <h2 class="employee-name">{{ store.employee.full_name }}</h2>
        <div class="employee-meta">
          <span class="employee-login">{{ store.employee.login }}</span>
          <span v-if="store.employee.phone" class="employee-phone">{{ store.employee.phone }}</span>
        </div>
      </div>
      <div class="employee-status-actions">
        <span :class="['status-badge', store.employee.status === 'active' ? 'status-active' : 'status-blocked']">
          {{ store.employee.status === 'active' ? 'Активний' : 'Заблокований' }}
        </span>
        <button class="btn-action btn-edit" @click="openEditDialog">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13M16 2L22 8M16 2V8M22 8H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Редагувати
        </button>
        <button
          v-if="store.employee.status === 'active'"
          class="btn-action btn-block"
          @click="toggleStatus"
        >
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M18.364 18.364L5.63605 5.63604M18.364 5.63604L5.63605 18.364" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          Заблокувати
        </button>
        <button
          v-else
          class="btn-action btn-unblock"
          @click="toggleStatus"
        >
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12L11 14L15 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="2"/>
          </svg>
          Розблокувати
        </button>
        <button class="btn-action btn-delete" @click="confirmDelete">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Видалити
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Grant All Button -->
      <div class="grant-all-section">
        <button class="btn btn-grant-all" @click="openGrantAllDialog">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M8.5 11a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M20 8v6M20 11H14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Надати всі паролі
        </button>
      </div>

      <!-- Granted Access Section -->
      <div class="access-section">
        <div class="section-header">
          <h3>Надані доступи ({{ store.credentials.length }})</h3>
        </div>

        <div v-if="store.credentials.length === 0" class="empty-state">
          <p>Доступів ще не надано</p>
        </div>

        <div v-for="cred in store.credentials" :key="cred.credential_id" class="access-row">
          <div class="access-service">
            <div class="service-icon" :style="{ backgroundColor: getServiceColor(cred.service_name) }">
              <img
                v-if="cred.service_logo_url"
                :src="cred.service_logo_url"
                :alt="cred.service_name"
                class="service-logo"
                @error="handleLogoError($event, cred)"
              />
              <span v-else class="service-letter">{{ cred.service_name.charAt(0).toUpperCase() }}</span>
            </div>
            <div class="service-info">
              <span class="service-name">{{ cred.service_name }}</span>
              <span class="service-url">{{ cred.service_url || '' }}</span>
            </div>
          </div>

          <div class="access-login">
            <div class="login-field">
              <span class="login-value">{{ cred.login }}</span>
              <button class="btn-copy" title="Копіювати" @click="copyToClipboard(cred.login)">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 5H6C5.46957 5 4.96086 5.21071 4.58579 5.58579C4.21071 5.96086 4 6.46957 4 7V16C4 16.5304 4.21071 17.0391 4.58579 17.4142C4.96086 17.7893 5.46957 18 6 18H9C9.53043 18 10.0391 17.7893 10.4142 17.4142C10.7893 17.0391 11 16.5304 11 16V7C11 6.46957 10.7893 5.96086 10.4142 5.58579C10.0391 5.21071 9.53043 5 9 5Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M14 5H20C20.5304 5 21.0391 5.21071 21.4142 5.58579C21.7893 5.96086 22 6.46957 22 7V16C22 16.5304 21.7893 17.0391 21.4142 17.4142C21.0391 17.7893 20.5304 18 20 18H14" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="access-password">
            <div class="password-field">
              <span v-if="cred.showPassword" class="password-value">{{ cred.protected_password }}</span>
              <span v-else class="password-dots">{{ '•'.repeat(Math.min(cred.protected_password.length, 12)) }}</span>
              <button class="btn-icon-small" :title="cred.showPassword ? 'Сховати' : 'Показати'" @click="togglePasswordVisibility(cred)">
                <svg v-if="cred.showPassword" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 12C13.1046 12 14 11.1046 14 10C14 8.89543 13.1046 8 12 8C10.8954 8 10 8.89543 10 10C10 11.1046 10.8954 12 12 12Z" stroke="currentColor" stroke-width="2"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17.94 17.94A10.07 10.07 0 013 12C3 12 7 4 12 4C14.53 4 16.95 5.02 18.94 6.58M1 1L23 23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </button>
              <button class="btn-icon-small" title="Копіювати" @click="copyToClipboard(cred.protected_password)">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 5H6C5.46957 5 4.96086 5.21071 4.58579 5.58579C4.21071 5.96086 4 6.46957 4 7V16C4 16.5304 4.21071 17.0391 4.58579 17.4142C4.96086 17.7893 5.46957 18 6 18H9C9.53043 18 10.0391 17.7893 10.4142 17.4142C10.7893 17.0391 11 16.5304 11 16V7C11 6.46957 10.7893 5.96086 10.4142 5.58579C10.0391 5.21071 9.53043 5 9 5Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M14 5H20C20.5304 5 21.0391 5.21071 21.4142 5.58579C21.7893 5.96086 22 6.46957 22 7V16C22 16.5304 21.7893 17.0391 21.4142 17.4142C21.0391 17.7893 20.5304 18 20 18H14" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="access-actions">
            <button class="btn-icon-small btn-grant-per-service" title="Надати доступ" @click="openGrantAccessForCredential(cred)">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8.5 11a4 4 0 100-8 4 4 0 000 8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M20 17v-2a4 4 0 00-3-3.87M20 21v-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
            <button class="btn-icon-small btn-delete-small" title="Видалити доступ" @click="revokeCredential(cred.credential_id)">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Grant Access Dialog -->
    <Teleport to="body">
      <div v-if="showGrantAccessDialog" class="modal-overlay" @click.self="closeGrantAccessDialog">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3>Надати доступ</h3>
            <button class="btn-close" @click="closeGrantAccessDialog">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div v-if="selectedCredentialForGrant" class="credential-info-card">
              <div class="credential-info-icon" :style="{ backgroundColor: getServiceColor(selectedCredentialForGrant.service_name) }">
                <img
                  v-if="selectedCredentialForGrant.service_logo_url"
                  :src="selectedCredentialForGrant.service_logo_url"
                  :alt="selectedCredentialForGrant.service_name"
                  class="service-logo-small"
                />
                <span v-else class="service-letter-small">{{ selectedCredentialForGrant.service_name.charAt(0).toUpperCase() }}</span>
              </div>
              <div class="credential-info-text">
                <span class="credential-info-service">{{ selectedCredentialForGrant.service_name }}</span>
                <span class="credential-info-login">{{ selectedCredentialForGrant.login }}</span>
              </div>
            </div>
            <div class="form-group">
              <label>Користувач</label>
              <div class="search-input-wrapper">
                <input
                  v-model="grantAccessSearch"
                  type="text"
                  placeholder="Пошук працівника..."
                  class="form-input"
                  @input="searchUsersForGrantAccess"
                />
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="search-icon">
                  <path d="M21 21L16.5 16.5M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
            <div v-if="grantAccessSearchResults.length > 0" class="search-results">
              <div
                v-for="user in grantAccessSearchResults"
                :key="user.user_id"
                class="search-result-item"
                @click="handleGrantAccessToUser(user.user_id)"
              >
                <div class="user-avatar-small" :style="{ backgroundColor: getAvatarColor(user.full_name || user.login || '?') }">
                  {{ getInitials(user.full_name || user.login || '?') }}
                </div>
                <div class="user-info-small">
                  <span class="user-name-small">{{ user.full_name }}</span>
                  <span class="user-login-small">{{ user.login }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="grantAccessSearch" class="no-results">
              <p>Нічого не знайдено</p>
            </div>
            <div v-else class="hint-text">
              <p>Введіть ім'я або логін працівника</p>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeGrantAccessDialog">Закрити</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Grant All Credentials Dialog -->
    <Teleport to="body">
      <div v-if="showGrantAllDialog" class="modal-overlay" @click.self="closeGrantAllDialog">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3>Надати всі паролі</h3>
            <button class="btn-close" @click="closeGrantAllDialog">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <p class="dialog-description">Усі паролі {{ store.employee?.full_name }} будуть надані обраному користувачеві.</p>
            <div class="form-group">
              <label>Користувач</label>
              <div class="search-input-wrapper">
                <input
                  v-model="grantAllSearch"
                  type="text"
                  placeholder="Пошук працівника..."
                  class="form-input"
                  @input="searchUsersForGrantAll"
                />
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="search-icon">
                  <path d="M21 21L16.5 16.5M11 19C15.4183 19 19 15.4183 19 11C19 6.58172 15.4183 3 11 3C6.58172 3 3 6.58172 3 11C3 15.4183 6.58172 19 11 19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
            </div>
            <div v-if="grantAllSearchResults.length > 0" class="search-results">
              <div
                v-for="user in grantAllSearchResults"
                :key="user.user_id"
                class="search-result-item"
                @click="handleGrantAllToUser(user.user_id)"
              >
                <div class="user-avatar-small" :style="{ backgroundColor: getAvatarColor(user.full_name || user.login || '?') }">
                  {{ getInitials(user.full_name || user.login || '?') }}
                </div>
                <div class="user-info-small">
                  <span class="user-name-small">{{ user.full_name }}</span>
                  <span class="user-login-small">{{ user.login }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="grantAllSearch" class="no-results">
              <p>Нічого не знайдено</p>
            </div>
            <div v-else class="hint-text">
              <p>Введіть ім'я або логін працівника</p>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeGrantAllDialog">Закрити</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Edit Employee Dialog -->
    <Teleport to="body">
      <div v-if="showEditDialog" class="modal-overlay" @click.self="closeEditDialog">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3>Редагувати працівника</h3>
            <button class="btn-close" @click="closeEditDialog">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>ПІБ</label>
              <input v-model="editForm.full_name" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Телефон</label>
              <input v-model="editForm.phone" type="text" class="form-input" placeholder="+380 XX XXX XX XX" />
            </div>
            <div class="form-group">
              <label>Логін</label>
              <input v-model="editForm.login" type="text" class="form-input" />
            </div>
            <div class="form-group">
              <label>Пароль</label>
              <div class="password-input-wrapper">
                <input :type="showEditPassword ? 'text' : 'password'" v-model="editForm.password" class="form-input" placeholder="Введіть новий пароль" />
                <button type="button" class="btn-password-toggle" @click="showEditPassword = !showEditPassword" :title="showEditPassword ? 'Сховати' : 'Показати'">
                  <svg v-if="!showEditPassword" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M1 1l22 22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeEditDialog">Скасувати</button>
            <button class="btn btn-primary" @click="handleEditEmployee">Зберегти</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Delete Confirmation Dialog -->
    <Teleport to="body">
      <div v-if="showDeleteDialog" class="modal-overlay" @click.self="showDeleteDialog = false">
        <div class="modal-dialog modal-small">
          <div class="modal-header">
            <h3>Видалити працівника?</h3>
            <button class="btn-close" @click="showDeleteDialog = false">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <p>Ви дійсно хочете видалити <strong>{{ store.employee?.full_name }}</strong>?</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showDeleteDialog = false">Скасувати</button>
            <button class="btn btn-danger" @click="handleDelete">Видалити</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEmployeeDetailStore } from '@/stores/employeeDetail'
import { useEmployeesStore } from '@/stores/employees'
import { useServicesStore } from '@/stores/services'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const store = useEmployeeDetailStore()
const employeesStore = useEmployeesStore()
const servicesStore = useServicesStore()
const authStore = useAuthStore()

const userId = computed(() => Number(route.params.id))

const avatarColors = [
  '#059669', '#2563eb', '#d97706', '#7c3aed', '#dc2626',
  '#0891b2', '#4f46e5', '#c026d3', '#ea580c', '#16a34a'
]

const serviceColors = [
  '#5865F2', '#EA4335', '#0078D4', '#181717', '#FF9900',
  '#00A4EF', '#4265B5', '#00B4E6', '#FF6C37', '#000000'
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

function getServiceColor(name: string): string {
  let hash = 0
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  return serviceColors[Math.abs(hash) % serviceColors.length] ?? '#5865F2'
}

function handleLogoError(event: Event, cred: any) {
  // Fallback to letter icon if image fails
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
  const letterSpan = img.nextElementSibling as HTMLSpanElement
  if (letterSpan) letterSpan.style.display = 'inline'
}

// Password visibility toggle per credential
function togglePasswordVisibility(cred: any) {
  cred.showPassword = !cred.showPassword
}

// Copy to clipboard
function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text).catch(() => {})
}

// Grant Access Dialog (for specific credential)
const showGrantAccessDialog = ref(false)
const grantAccessSearch = ref('')
const grantAccessSearchResults = ref<Array<{ user_id: number; full_name: string | null; login: string | null }>>([])
const selectedCredentialForGrant = ref<any>(null)

function openGrantAccessForCredential(cred: any) {
  selectedCredentialForGrant.value = cred
  showGrantAccessDialog.value = true
  grantAccessSearch.value = ''
  grantAccessSearchResults.value = []
}

function closeGrantAccessDialog() {
  showGrantAccessDialog.value = false
  grantAccessSearch.value = ''
  grantAccessSearchResults.value = []
  selectedCredentialForGrant.value = null
}

async function searchUsersForGrantAccess() {
  if (!grantAccessSearch.value || grantAccessSearch.value.length < 1) {
    grantAccessSearchResults.value = []
    return
  }
  const token = authStore.token
  if (!token) return
  try {
    const response = await fetch(`/api/users/?search=${encodeURIComponent(grantAccessSearch.value)}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    if (response.ok) {
      const allUsers = await response.json()
      // Виключаємо поточного користувача з пошуку
      grantAccessSearchResults.value = allUsers.filter((u: any) => u.user_id !== userId.value)
    }
  } catch {
    // Ігноруємо помилки пошуку
  }
}

async function handleGrantAccessToUser(targetUserId: number) {
  if (!selectedCredentialForGrant.value) return
  const result = await store.grantCredential(targetUserId, {
    service_id: selectedCredentialForGrant.value.service_id,
    login: selectedCredentialForGrant.value.login,
    password: selectedCredentialForGrant.value.protected_password,
    comment: selectedCredentialForGrant.value.comment || undefined
  })
  if (result) {
    closeGrantAccessDialog()
    await store.fetchCredentials(userId.value)
  }
}

// Grant All Credentials Dialog
const showGrantAllDialog = ref(false)
const grantAllSearch = ref('')
const grantAllSearchResults = ref<Array<{ user_id: number; full_name: string | null; login: string | null }>>([])

function openGrantAllDialog() {
  showGrantAllDialog.value = true
  grantAllSearch.value = ''
  grantAllSearchResults.value = []
}

function closeGrantAllDialog() {
  showGrantAllDialog.value = false
  grantAllSearch.value = ''
  grantAllSearchResults.value = []
}

async function searchUsersForGrantAll() {
  if (!grantAllSearch.value || grantAllSearch.value.length < 1) {
    grantAllSearchResults.value = []
    return
  }
  const token = authStore.token
  if (!token) return
  try {
    const response = await fetch(`/api/users/?search=${encodeURIComponent(grantAllSearch.value)}`,
      { headers: { 'Authorization': `Bearer ${token}` } }
    )
    if (response.ok) {
      const allUsers = await response.json()
      // Виключаємо поточного користувача з пошуку
      grantAllSearchResults.value = allUsers.filter((u: any) => u.user_id !== userId.value)
    }
  } catch {
    // Ігноруємо помилки пошуку
  }
}

async function handleGrantAllToUser(targetUserId: number) {
  const result = await store.grantAllCredentialsToUser(targetUserId, userId.value)
  if (result) {
    closeGrantAllDialog()
  }
}

// Revoke credential
async function revokeCredential(credential_id: number) {
  const success = await store.revokeCredential(userId.value, credential_id)
  if (success) {
    await store.fetchEmployee(userId.value)
  }
}

// Edit dialog
const showEditDialog = ref(false)
const showEditPassword = ref(false)
const editForm = ref({
  full_name: '',
  phone: '',
  login: '',
  password: ''
})

function openEditDialog() {
  if (!store.employee) return
  showEditDialog.value = true
  showEditPassword.value = false
  editForm.value = {
    full_name: store.employee.full_name || '',
    phone: store.employee.phone || '',
    login: store.employee.login || '',
    password: ''
  }
}

function closeEditDialog() {
  showEditDialog.value = false
  showEditPassword.value = false
}

async function handleEditEmployee() {
  if (!store.employee || !editForm.value.full_name) return
  const result = await store.updateEmployee(store.employee.user_id, {
    full_name: editForm.value.full_name,
    phone: editForm.value.phone || undefined,
    login: editForm.value.login || undefined,
    password: editForm.value.password || undefined
  })
  if (result) {
    closeEditDialog()
  }
}

// Toggle status
async function toggleStatus() {
  if (!store.employee) return
  const newStatus = store.employee.status === 'active' ? 'blocked' : 'active'
  const result = await employeesStore.updateStatus(store.employee.user_id, newStatus)
  if (result) {
    store.employee.status = newStatus
  }
}

// Delete dialog
const showDeleteDialog = ref(false)

function confirmDelete() {
  showDeleteDialog.value = true
}

async function handleDelete() {
  if (!store.employee) return
  const result = await employeesStore.deleteEmployee(store.employee.user_id)
  if (result) {
    showDeleteDialog.value = false
    router.push('/users')
  }
}

onMounted(async () => {
  await Promise.all([
    store.fetchEmployee(userId.value),
    store.fetchCredentials(userId.value),
    servicesStore.fetchServices()
  ])
})
</script>

<style scoped>
.employee-detail-view {
  width: 100%;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: none;
  border: none;
  color: #0d9488;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  margin-bottom: 1.5rem;
  transition: color 0.15s;
}

.btn-back:hover {
  color: #0f766e;
}

.btn-back svg {
  width: 16px;
  height: 16px;
}

/* Employee Card */
.employee-card {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background: #fff;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
}

.employee-avatar-large {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.employee-details {
  flex: 1;
}

.employee-name {
  margin: 0;
  font-size: 1.25rem;
  color: #0f172a;
}

.employee-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.25rem;
  font-size: 0.875rem;
  color: #64748b;
}

.employee-status-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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

.btn-action {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  background: #fff;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
}

.btn-action svg {
  width: 16px;
  height: 16px;
}

.btn-edit {
  color: #475569;
}

.btn-edit:hover {
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
}

.btn-delete:hover {
  background: #fee2e2;
}

/* Main Content */
.main-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Grant All Section */
.grant-all-section {
  display: flex;
  justify-content: flex-end;
}

.grant-all-section .btn-grant-all {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: #2563eb;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s;
}

.grant-all-section .btn-grant-all:hover {
  background: #1d4ed8;
}

.grant-all-section .btn-grant-all svg {
  width: 18px;
  height: 18px;
}

/* Access Section */
.access-section {
  background: #fff;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
}

.section-header h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  color: #0f172a;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: #94a3b8;
}

.access-row {
  display: grid;
  grid-template-columns: 200px 1fr 1fr auto;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  margin-bottom: 0.75rem;
  align-items: center;
}

.access-row:last-child {
  margin-bottom: 0;
}

.access-service {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.service-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.service-logo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}

.service-letter {
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
}

.service-info {
  display: flex;
  flex-direction: column;
}

.service-name {
  font-weight: 600;
  font-size: 0.875rem;
  color: #0f172a;
}

.service-url {
  font-size: 0.75rem;
  color: #94a3b8;
}

.access-login, .access-password {
  display: flex;
  align-items: center;
}

.login-field, .password-field {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  flex: 1;
}

.login-value {
  font-size: 0.875rem;
  color: #0f172a;
  flex: 1;
}

.password-dots {
  font-size: 0.875rem;
  color: #0f172a;
  flex: 1;
  letter-spacing: 0.1em;
}

.password-value {
  font-size: 0.875rem;
  color: #0f172a;
  flex: 1;
  font-family: monospace;
  word-break: break-all;
}

.btn-copy {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  transition: color 0.15s;
}

.btn-copy:hover {
  color: #475569;
}

.btn-copy svg {
  width: 16px;
  height: 16px;
}

.btn-icon-small {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  transition: color 0.15s;
}

.btn-icon-small:hover {
  color: #475569;
}

.btn-icon-small svg {
  width: 16px;
  height: 16px;
}

.access-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-delete-small {
  color: #dc2626;
  background: #fef2f2;
  border-radius: 0.375rem;
}

.btn-delete-small:hover {
  color: #b91c1c;
  background: #fee2e2;
}

.btn-grant-per-service {
  color: #0d9488;
  background: #f0fdfa;
  border-radius: 0.375rem;
}

.btn-grant-per-service:hover {
  color: #0f766e;
  background: #ccfbf1;
}

/* Search input in dialogs */
.search-input-wrapper {
  position: relative;
}

.search-input-wrapper .form-input {
  padding-right: 2.5rem;
}

.search-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #94a3b8;
  pointer-events: none;
}

.search-results {
  max-height: 240px;
  overflow-y: auto;
  margin-top: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  cursor: pointer;
  transition: background-color 0.15s;
}

.search-result-item:hover {
  background: #f1f5f9;
}

.search-result-item:not(:last-child) {
  border-bottom: 1px solid #f1f5f9;
}

.user-avatar-small {
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

.user-info-small {
  display: flex;
  flex-direction: column;
}

.user-name-small {
  font-size: 0.875rem;
  font-weight: 500;
  color: #0f172a;
}

.user-login-small {
  font-size: 0.75rem;
  color: #94a3b8;
}

.no-results {
  padding: 1.5rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

.hint-text {
  padding: 1.5rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

.dialog-description {
  margin: 0 0 1rem;
  color: #475569;
  font-size: 0.875rem;
  line-height: 1.5;
}

/* Credential Info Card in Grant Dialog */
.credential-info-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  margin-bottom: 1rem;
}

.credential-info-icon {
  width: 40px;
  height: 40px;
  border-radius: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.service-logo-small {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0.5rem;
}

.service-letter-small {
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
}

.credential-info-text {
  display: flex;
  flex-direction: column;
}

.credential-info-service {
  font-weight: 600;
  font-size: 0.875rem;
  color: #0f172a;
}

.credential-info-login {
  font-size: 0.75rem;
  color: #64748b;
}

.grant-form-card {
  background: #fff;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  padding: 1.5rem;
}

.grant-form-card h3 {
  margin: 0 0 1rem;
  font-size: 1rem;
  color: #0f172a;
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

.form-input {
  width: 100%;
  padding: 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #2563eb;
}

.form-select {
  width: 100%;
  padding: 0.625rem 2rem 0.625rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  cursor: pointer;
  background: #fff;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.password-input-wrapper {
  position: relative;
}

.password-input-wrapper .form-input {
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

.btn-grant {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.625rem 1.25rem;
  background: #0d9488;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.15s;
}

.btn-grant:hover:not(:disabled) {
  background: #0f766e;
}

.btn-grant:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-grant svg {
  width: 16px;
  height: 16px;
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

@media (max-width: 1024px) {
  .access-row {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
}
</style>
