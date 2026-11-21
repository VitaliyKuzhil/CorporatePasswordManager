<template>
  <div class="service-detail-page">
    <!-- Back Button -->
    <button class="back-btn" @click="goBack">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      До списку джерел
    </button>

    <!-- Loading State -->
    <div v-if="detailStore.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Завантаження...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="detailStore.error" class="error-state">
      <p>{{ detailStore.error }}</p>
      <button class="btn btn-secondary" @click="goBack">Повернутися</button>
    </div>

    <!-- Service Detail Content -->
    <template v-else-if="detailStore.detail">
      <div class="detail-header">
        <div class="service-title-row">
          <div class="service-avatar" :style="{ backgroundColor: serviceColor }">
            <img
              v-if="detailStore.detail.service_logo_url"
              :src="detailStore.detail.service_logo_url"
              :alt="detailStore.detail.service_name"
              class="service-avatar-img"
              @error="handleAvatarError"
            />
            <span v-else class="avatar-letter">{{ getInitials(detailStore.detail.service_name) }}</span>
          </div>
          <div class="service-title-info">
            <h1 class="service-name">{{ detailStore.detail.service_name }}</h1>
            <p class="service-description">
              Паролі для {{ detailStore.detail.service_name }}, які мають до них доступ
            </p>
          </div>
        </div>

        <!-- Session Timer -->
        <div class="session-timer-badge">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 8V12L15 15M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Сесія ще {{ sessionTimeLeft }}
        </div>
      </div>

      <!-- Service Info Card -->
      <div class="service-info-card">
        <div class="service-info-left">
          <div class="service-avatar-large" :style="{ backgroundColor: serviceColor }">
            <img
              v-if="detailStore.detail.service_logo_url"
              :src="detailStore.detail.service_logo_url"
              :alt="detailStore.detail.service_name"
              class="service-avatar-img"
              @error="handleAvatarError"
            />
            <span v-else class="avatar-letter">{{ getInitials(detailStore.detail.service_name) }}</span>
          </div>
          <div class="service-info-text">
            <h2 class="info-service-name">{{ detailStore.detail.service_name }}</h2>
            <a
              v-if="detailStore.detail.service_url"
              :href="detailStore.detail.service_url"
              target="_blank"
              rel="noopener noreferrer"
              class="service-url"
            >
              {{ getServiceDomain(detailStore.detail.service_url) }}
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 13V19C18 20.1046 17.1046 21 16 21H8C6.89543 21 6 20.1046 6 19V13M12 3L12 4M12 3L9 6M12 3L15 6M15 19H21M3 19H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
          </div>
        </div>

        <div class="service-info-actions">
          <button class="btn btn-generate" @click="openGeneratePassword">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Згенерувати пароль
          </button>
          <button v-if="isAdmin" class="btn btn-edit" @click="editService">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Редагувати
          </button>
          <button v-if="isAdmin" class="btn btn-delete" @click="deleteService">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Видалити
          </button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="stats-row">
        <div class="stat-card">
          <div class="stat-icon passwords">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 15V17M12 11H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ detailStore.detail.credential_count }}</div>
            <div class="stat-label">Паролів у джерелі</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon access">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 16.7909 15.2091 15 13 15H5C2.79086 15 1 16.7909 1 19V21M21 11C21 15.4183 15.4183 21 11 21C6.58172 21 1 15.4183 1 11C1 6.58172 6.58172 1 11 1C15.4183 1 21 6.58172 21 11ZM16 7L12 11M12 11L8 7M12 11V5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ detailStore.detail.access_count }}</div>
            <div class="stat-label">Надамо доступу</div>
          </div>
        </div>
      </div>

      <!-- Credentials Table -->
      <div class="credentials-section">
        <div class="section-header">
          <h3 class="section-title">Паролі джерела ({{ detailStore.detail.credential_count }})</h3>
        </div>

        <div class="credentials-table-wrapper">
          <table class="credentials-table">
            <thead>
              <tr>
                <th>Назва</th>
                <th>Логін</th>
                <th>Пароль</th>
                <th>Коментар</th>
                <th>Користувачі</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="detailStore.detail.credentials.length === 0">
                <td colspan="5" class="empty-credentials">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 15V17M12 11H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <p>Паролі ще не додано</p>
                </td>
              </tr>
              <tr v-for="(cred, index) in detailStore.detail.credentials" :key="cred.credential_id" class="credential-row">
                <td class="cred-name">{{ getCredentialName(cred, index) }}</td>
                <td class="cred-login">{{ cred.login || '—' }}</td>
                <td class="cred-password">
                  <div class="password-cell">
                    <span v-if="visiblePasswords.has(cred.credential_id)" class="password-value">{{ cred.protected_password }}</span>
                    <span v-else class="password-dots">••••••••••</span>
                    <button class="btn-icon-sm" @click="togglePassword(cred.credential_id)" :title="visiblePasswords.has(cred.credential_id) ? 'Сховати' : 'Показати'">
                      <svg v-if="visiblePasswords.has(cred.credential_id)" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20C7 20 3 16 3 11C3 8.44 4.06 6.11 5.82 4.5M18.62 4.5C16.86 6.11 15.8 8.44 15.8 11C15.8 16 19.8 20 24.8 20C22.8 20 20.8 19.2 19.18 17.94M1 1L23 23M7.88 7.88C7.3 8.46 6.8 9.18 6.4 10M12 12C12 12.5523 11.5523 13 11 13C10.4477 13 10 12.5523 10 12C10 11.4477 10.4477 11 11 11C11.5523 11 12 11.4477 12 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12ZM12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                    <button class="btn-icon-sm" @click="copyPassword(cred.credential_id)" title="Копіювати">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M9 6H6C4.89543 6 4 6.89543 4 8V18C4 19.1046 4.89543 20 6 20H14C15.1046 20 16 19.1046 16 18V15M12 6H15C16.1046 6 17 6.89543 17 8V14C17 15.1046 16.1046 16 15 16H12V6Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                  </div>
                </td>
                <td class="cred-comment">{{ cred.comment || '—' }}</td>
                <td class="cred-users">
                  <button class="access-btn" @click="openAccessDialog(cred.credential_id, cred.comment || '')">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M17 21V19C17 16.7909 15.2091 15 13 15H5C2.79086 15 1 16.7909 1 19V21M21 11C21 15.4183 15.4183 21 11 21C6.58172 21 1 15.4183 1 11C1 6.58172 6.58172 1 11 1C15.4183 1 21 6.58172 21 11ZM16 7L12 11M12 11L8 7M12 11V5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <span class="access-count">{{ cred.access_count }}</span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </template>

    <!-- Add Credential Dialog -->
    <div v-if="showAddDialog" class="dialog-overlay" @click.self="closeAddDialog">
      <div class="add-dialog">
        <div class="add-dialog-header">
          <div>
            <h3 class="add-dialog-title">Додати пароль</h3>
            <p class="add-dialog-subtitle">{{ detailStore.detail?.service_name || '' }}</p>
          </div>
          <button class="btn-close" @click="closeAddDialog">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <div class="add-dialog-body">
          <!-- Name Field -->
          <div class="form-group">
            <label class="form-label">Назва</label>
            <input
              v-model="addForm.name"
              type="text"
              placeholder="Наприклад, Основний акаунт"
              class="form-input"
            />
          </div>

          <!-- Login Field -->
          <div class="form-group">
            <label class="form-label">Логін</label>
            <input
              v-model="addForm.login"
              type="text"
              placeholder="email@company.com"
              class="form-input"
            />
          </div>

          <!-- Password Field -->
          <div class="form-group">
            <label class="form-label">Пароль</label>
            <div class="password-input-wrapper">
              <input
                :type="addPasswordVisible ? 'text' : 'password'"
                v-model="addForm.password"
                class="form-input password-input"
                readonly
              />
              <div class="password-actions">
                <button class="btn-icon-sm" @click="addPasswordVisible = !addPasswordVisible" title="Показати пароль">
                  <svg v-if="addPasswordVisible" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20C7 20 3 16 3 11C3 8.44 4.06 6.11 5.82 4.5M18.62 4.5C16.86 6.11 15.8 8.44 15.8 11C15.8 16 19.8 20 24.8 20C22.8 20 20.8 19.2 19.18 17.94M1 1L23 23M7.88 7.88C7.3 8.46 6.8 9.18 6.4 10M12 12C12 12.5523 11.5523 13 11 13C10.4477 13 10 12.5523 10 12C10 11.4477 10.4477 11 11 11C11.5523 11 12 11.4477 12 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12ZM12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="btn-icon-sm" @click="generateAddPassword" title="Згенерувати пароль">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M4 4V9H9M9 4V9H4M15 4H20V9M20 4V9H15M4 15V20H9M9 15V20H4M15 15H20V20M20 15V20H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button class="btn-icon-sm" @click="copyAddPassword" title="Копіювати">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 6H6C4.89543 6 4 6.89543 4 8V18C4 19.1046 4.89543 20 6 20H14C15.1046 20 16 19.1046 16 18V15M12 6H15C16.1046 6 17 6.89543 17 8V14C17 15.1046 16.1046 16 15 16H12V6Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Comment Field -->
          <div class="form-group">
            <label class="form-label">Коментар</label>
            <input
              v-model="addForm.comment"
              type="text"
              placeholder="Додаткова інформація"
              class="form-input"
            />
          </div>

          <!-- Grant Access Section -->
          <div class="grant-access-section">
            <h4 class="grant-access-title">Надати доступ</h4>

            <!-- Selected Users -->
            <div v-if="addSelectedUsers.length > 0" class="selected-users-list">
              <div v-for="userId in addSelectedUsers" :key="userId" class="selected-user-item">
                <div class="selected-user-avatar" :style="{ backgroundColor: getSelectedUserColor(userId) }">
                  <span class="selected-user-avatar-letter">{{ getInitials(getSelectedUserDisplayName(userId)) }}</span>
                </div>
                <div class="selected-user-info">
                  <span class="selected-user-name">{{ getSelectedUserDisplayName(userId) }}</span>
                </div>
                <button class="btn-remove-selected" @click="removeSelectedUser(userId)" title="Видалити">
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- User Search -->
            <div class="user-search-wrapper">
              <input
                v-model="addUserSearchQuery"
                @input="onAddUserSearch"
                type="text"
                placeholder="Пошук працівника..."
                class="user-search-input"
              />
              <div v-if="addUserSearchQuery && addSearchResults.length > 0" class="search-results">
                <div
                  v-for="user in addSearchResults"
                  :key="user.user_id"
                  class="search-result-item"
                  @click="selectAddUser(user.user_id)"
                >
                  <div class="search-user-avatar" :style="{ backgroundColor: getUserColor(user.user_id) }">
                    <span class="search-user-avatar-letter">{{ getInitials(user.full_name || user.login || '') }}</span>
                  </div>
                  <div class="search-user-info">
                    <span class="search-user-name">{{ user.full_name || 'Без імені' }}</span>
                    <span class="search-user-login">{{ user.login || '' }}</span>
                  </div>
                </div>
              </div>
              <div v-else-if="addUserSearchQuery && addSearchResults.length === 0" class="no-results">
                Нічого не знайдено
              </div>
            </div>
          </div>
        </div>

        <!-- Dialog Footer -->
        <div class="add-dialog-footer">
          <button class="btn btn-add-submit" :disabled="credentialsStore.loading" @click="submitAddCredential">
            <svg v-if="!credentialsStore.loading" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span v-if="credentialsStore.loading">Збереження...</span>
            <span v-else>+ Зберегти</span>
          </button>
          <button class="btn btn-cancel" @click="closeAddDialog">Закрити</button>
        </div>
      </div>
    </div>

    <!-- Edit Service Dialog -->
    <div v-if="showEditDialog" class="dialog-overlay" @click.self="closeEditDialog">
      <div class="edit-service-dialog">
        <div class="edit-dialog-header">
          <h3 class="edit-dialog-title">Редагувати джерело</h3>
          <button class="btn-close" @click="closeEditDialog">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <div class="edit-dialog-body">
          <div class="form-group">
            <label class="form-label">Назва джерела *</label>
            <input
              v-model="editForm.service_name"
              type="text"
              class="form-input"
              placeholder="Назва джерела"
            />
          </div>

          <div class="form-group">
            <label class="form-label">URL</label>
            <input
              v-model="editForm.service_url"
              type="text"
              class="form-input"
              placeholder="https://example.com/"
            />
          </div>

          <div class="form-group">
            <label class="form-label">URL логотипу</label>
            <input
              v-model="editForm.service_logo_url"
              type="text"
              class="form-input"
              placeholder="https://example.com/logo.png"
            />
          </div>
        </div>

        <div class="edit-dialog-footer">
          <button class="btn btn-secondary" @click="closeEditDialog">Скасувати</button>
          <button class="btn btn-primary" :disabled="servicesStore.loading" @click="submitEditService">
            {{ servicesStore.loading ? 'Збереження...' : 'Зберегти' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Access Dialog -->
    <div v-if="showAccessDialog" class="dialog-overlay" @click.self="closeAccessDialog">
      <div class="access-dialog">
        <div class="access-dialog-header">
          <div>
            <h3 class="access-dialog-title">{{ accessDialogTitle }}</h3>
            <p class="access-dialog-subtitle">{{ currentCredentialName }}</p>
          </div>
          <button class="btn-close" @click="closeAccessDialog">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>

        <!-- Users with access -->
        <div class="access-list-section">
          <h4 class="access-section-title">Мають доступ ({{ accessStore.usersWithAccess.length }})</h4>
          <div v-if="accessStore.loading" class="access-loading">Завантаження...</div>
          <div v-else-if="accessStore.usersWithAccess.length === 0" class="access-empty">
            Наразі ніхто не має доступу
          </div>
          <div v-else class="access-list">
            <div v-for="user in accessStore.usersWithAccess" :key="user.user_id" class="access-user-item">
              <div class="access-user-avatar" :style="{ backgroundColor: getUserColor(user.user_id) }">
                <img
                  v-if="user.avatar_url"
                  :src="user.avatar_url"
                  :alt="user.full_name || user.login || ''"
                  class="access-user-avatar-img"
                  @error="handleUserAvatarError"
                />
                <span v-else class="access-user-avatar-letter">{{ getInitials(user.full_name || user.login || '') }}</span>
              </div>
              <div class="access-user-info">
                <span class="access-user-name">{{ user.full_name || 'Без імені' }}</span>
                <span class="access-user-login">{{ user.login || '' }}</span>
              </div>
              <button v-if="isAdmin" class="btn-remove-access" @click="removeAccess(user.user_id)" title="Забрати доступ">
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 6H5H21M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Add user search -->
        <div v-if="isAdmin" class="add-user-section">
          <h4 class="access-section-title">Додати користувача</h4>
          <div class="user-search-wrapper">
            <input
              v-model="userSearchQuery"
              @input="onUserSearch"
              type="text"
              placeholder="Пошук працівника..."
              class="user-search-input"
            />
            <div v-if="userSearchQuery && accessStore.searchResults.length > 0" class="search-results">
              <div
                v-for="user in accessStore.searchResults"
                :key="user.user_id"
                class="search-result-item"
                @click="addUserAccess(user.user_id)"
              >
                <div class="search-user-avatar" :style="{ backgroundColor: getUserColor(user.user_id) }">
                  <span class="search-user-avatar-letter">{{ getInitials(user.full_name || user.login || '') }}</span>
                </div>
                <div class="search-user-info">
                  <span class="search-user-name">{{ user.full_name || 'Без імені' }}</span>
                  <span class="search-user-login">{{ user.login || '' }}</span>
                </div>
              </div>
            </div>
            <div v-else-if="userSearchQuery && accessStore.searchResults.length === 0" class="no-results">
              Нічого не знайдено
            </div>
          </div>
        </div>

        <!-- Close button -->
        <div class="access-dialog-footer">
          <button class="btn btn-close-dialog" @click="closeAccessDialog">Закрити</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useServiceDetailStore } from '@/stores/serviceDetail'
import { useServicesStore } from '@/stores/services'
import { useAccessStore } from '@/stores/access'
import { useCredentialsStore } from '@/stores/credentials'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const detailStore = useServiceDetailStore()
const servicesStore = useServicesStore()
const accessStore = useAccessStore()
const credentialsStore = useCredentialsStore()

const isAdmin = computed(() => authStore.user?.role === 'admin')
const visiblePasswords = ref<Set<number>>(new Set())

const accessDialogTitle = computed(() => {
  return currentCredentialId.value === null ? 'Надати доступ' : 'Доступ до пароля'
})

// Access dialog state
const showAccessDialog = ref(false)
const currentCredentialId = ref<number | null>(null)
const currentCredentialName = ref('')
const userSearchQuery = ref('')

// Edit service dialog state
const showEditDialog = ref(false)
const editForm = ref({
  service_name: '',
  service_url: '',
  service_logo_url: ''
})

function openEditDialog() {
  if (!detailStore.detail) return
  showEditDialog.value = true
  editForm.value = {
    service_name: detailStore.detail.service_name || '',
    service_url: detailStore.detail.service_url || '',
    service_logo_url: detailStore.detail.service_logo_url || ''
  }
}

function closeEditDialog() {
  showEditDialog.value = false
}

async function submitEditService() {
  if (!detailStore.detail || !editForm.value.service_name) return
  const result = await servicesStore.updateService(detailStore.detail.service_id, {
    service_name: editForm.value.service_name,
    service_url: editForm.value.service_url || undefined,
    service_logo_url: editForm.value.service_logo_url || undefined
  })
  if (result) {
    await detailStore.fetchServiceDetail(serviceId.value)
    closeEditDialog()
  }
}

// Add credential dialog state
const showAddDialog = ref(false)
const addForm = ref({
    name: '',
    login: '',
    password: '',
    comment: ''
})
const addSelectedUsers = ref<number[]>([])
const addUserSearchQuery = ref('')
const addSearchResults = ref<any[]>([])
const addPasswordVisible = ref(false)

const serviceId = computed(() => Number(route.params.id))

const serviceColor = computed(() => {
  const colors = ['#5865F2', '#EA4335', '#0052CC', '#24292E', '#FF6C37', '#1DA1F2', '#0073B1', '#E60023', '#4267B2', '#000000']
  const index = (serviceId.value - 1) % colors.length
  return colors[index]!
})

const sessionTimeLeft = computed(() => {
  const hours = 11
  const minutes = 42
  return `${hours} год ${minutes} хв`
})

function getInitials(name: string) {
  return name.charAt(0).toUpperCase()
}

function getServiceDomain(url: string): string {
  try {
    const parsed = new URL(url)
    return parsed.hostname.replace('www.', '')
  } catch {
    return url
  }
}

function getCredentialName(cred: { login: string | null; comment: string | null }, index: number): string {
  if (cred.comment) {
    const parts = cred.comment.split(' ')
    if (parts.length >= 2) {
      return parts.slice(0, 2).join(' ')
    }
  }
  return `Пароль ${index + 1}`
}

function handleAvatarError(e: Event) {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
  const fallback = img.nextElementSibling as HTMLElement | null
  if (fallback) {
    fallback.style.display = 'flex'
  }
}

function togglePassword(credentialId: number) {
  if (visiblePasswords.value.has(credentialId)) {
    visiblePasswords.value.delete(credentialId)
  } else {
    visiblePasswords.value.add(credentialId)
  }
}

function copyPassword(credentialId: number) {
  // TODO: реалізувати копіювання пароля
  console.log('Копіювати пароль:', credentialId)
}

function openGeneratePassword() {
  showAddDialog.value = true
  addForm.value = { name: '', login: '', password: '', comment: '' }
  addSelectedUsers.value = []
  addUserSearchQuery.value = ''
  addSearchResults.value = []
  addPasswordVisible.value = false
  generateAddPassword()
}

function openGrantAccess() {
  // Відкрити діалог доступу на рівні сервісу (без конкретного креденшала)
  currentCredentialId.value = null
  currentCredentialName.value = detailStore.detail?.service_name || ''
  showAccessDialog.value = true
  userSearchQuery.value = ''
  accessStore.searchResults = []
  // Для сервісного рівня, показуємо унікальних користувачів з усіх креденшалів
  if (detailStore.detail?.credentials) {
    const allUserIds = new Set<number>()
    detailStore.detail.credentials.forEach((cred: any) => {
      // Користувачі з доступом до будь-якого креденшала цього сервісу
    })
  }
}

function editService() {
  openEditDialog()
}

async function deleteService() {
  if (!detailStore.detail) return
  if (!confirm('Видалити це джерело?')) return
  const result = await servicesStore.deleteService(detailStore.detail.service_id)
  if (result) {
    router.push('/')
  }
}


function closeAddDialog() {
  showAddDialog.value = false
  credentialsStore.clearError()
}

function generateAddPassword() {
  const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
  let password = ''
  for (let i = 0; i < 24; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  addForm.value.password = password
}

async function onAddUserSearch() {
  if (addUserSearchQuery.value.length >= 1) {
    await accessStore.searchUsers(addUserSearchQuery.value)
    // Фільтруємо тих, хто вже обраний
    addSearchResults.value = accessStore.searchResults.filter(
      (u: any) => !addSelectedUsers.value.includes(u.user_id)
    )
  } else {
    addSearchResults.value = []
  }
}

function selectAddUser(userId: number) {
  if (!addSelectedUsers.value.includes(userId)) {
    addSelectedUsers.value.push(userId)
  }
  addUserSearchQuery.value = ''
  addSearchResults.value = []
}

function removeSelectedUser(userId: number) {
  addSelectedUsers.value = addSelectedUsers.value.filter(id => id !== userId)
}

async function submitAddCredential() {
  if (!addForm.value.password) return
  const result = await credentialsStore.createCredential(serviceId.value, {
    login: addForm.value.login,
    password: addForm.value.password,
    comment: addForm.value.comment,
    user_ids: addSelectedUsers.value
  })
  if (result) {
    closeAddDialog()
    // Оновлюємо деталі сервісу
    detailStore.fetchServiceDetail(serviceId.value)
  }
}

function getSelectedUserDisplayName(userId: number): string {
  // Спочатку шукаємо в результатах пошуку
  const allUsers = [...accessStore.usersWithAccess, ...accessStore.searchResults, ...addSearchResults.value]
  const user = allUsers.find((u: any) => u.user_id === userId)
  if (user) return user.full_name || user.login || ''
  // Якщо не знайдено, повертаємо з доступу
  const accessUser = accessStore.usersWithAccess.find((u: any) => u.user_id === userId)
  if (accessUser) return accessUser.full_name || accessUser.login || ''
  return `Користувач #${userId}`
}

function getSelectedUserColor(userId: number): string {
  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#64748b', '#ef4444', '#ec4899', '#14b8a6']
  return colors[userId % colors.length]!
}

function copyAddPassword() {
  navigator.clipboard.writeText(addForm.value.password).then(() => {
    console.log('Пароль скопійовано')
  }).catch(() => {
    console.log('Не вдалося скопіювати пароль')
  })
}

function goBack() {
  router.push('/')
}

// Access dialog functions
function openAccessDialog(credentialId: number, comment: string) {
  currentCredentialId.value = credentialId
  currentCredentialName.value = comment || `Пароль #${credentialId}`
  showAccessDialog.value = true
  userSearchQuery.value = ''
  accessStore.clearAccess()
  if (serviceId.value && credentialId) {
    accessStore.fetchUsersWithAccess(serviceId.value, credentialId)
  }
}

function closeAccessDialog() {
  showAccessDialog.value = false
  currentCredentialId.value = null
  currentCredentialName.value = ''
  userSearchQuery.value = ''
  accessStore.clearAccess()
}

function onUserSearch() {
  if (userSearchQuery.value.length >= 1) {
    accessStore.searchUsers(userSearchQuery.value)
  } else {
    accessStore.searchResults = []
  }
}

async function addUserAccess(userId: number) {
  if (!currentCredentialId.value) return
  const success = await accessStore.grantAccess(serviceId.value, currentCredentialId.value, userId)
  if (success) {
    userSearchQuery.value = ''
    accessStore.searchResults = []
    // Оновлюємо детальну інформацію про сервіс
    await detailStore.fetchServiceDetail(serviceId.value)
  }
}

async function removeAccess(userId: number) {
  if (!currentCredentialId.value) return
  const success = await accessStore.revokeAccess(serviceId.value, currentCredentialId.value, userId)
  if (success) {
    // Оновлюємо детальну інформацію про сервіс
    await detailStore.fetchServiceDetail(serviceId.value)
  }
}

function getUserColor(userId: number): string {
  const colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#64748b', '#ef4444', '#ec4899', '#14b8a6']
  return colors[userId % colors.length]!
}

function handleUserAvatarError(e: Event) {
  const img = e.target as HTMLImageElement
  img.style.display = 'none'
  const fallback = img.nextElementSibling as HTMLElement | null
  if (fallback) {
    fallback.style.display = 'flex'
  }
}

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchProfile()
  }
  detailStore.fetchServiceDetail(serviceId.value)
})
</script>

<style scoped>
.service-detail-page {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Back Button */
.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  color: #64748b;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: color 0.2s;
}

.back-btn:hover {
  color: #0f172a;
}

.back-btn svg {
  width: 18px;
  height: 18px;
}

/* Loading & Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #64748b;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #5865F2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Detail Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.service-title-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.service-avatar {
  width: 48px;
  height: 48px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.service-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-letter {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.service-title-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.service-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.service-description {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0;
}

.session-timer-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  color: #64748b;
}

.session-timer-badge svg {
  width: 16px;
  height: 16px;
}

/* Service Info Card */
.service-info-card {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.service-info-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.service-avatar-large {
  width: 56px;
  height: 56px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.service-info-text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-service-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.service-url {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  color: #64748b;
  font-size: 0.875rem;
  text-decoration: none;
  transition: color 0.2s;
}

.service-url:hover {
  color: #5865F2;
}

.service-url svg {
  width: 14px;
  height: 14px;
}

.service-info-actions {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* Stats Row */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  border-radius: 1rem;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 52px;
  height: 52px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 26px;
  height: 26px;
}

.stat-icon.passwords {
  background: #e0f2fe;
  color: #0284c7;
}

.stat-icon.access {
  background: #dcfce7;
  color: #16a34a;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
}

.stat-label {
  font-size: 0.875rem;
  color: #64748b;
}

/* Credentials Section */
.credentials-section {
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: relative;
}

.section-header {
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.credentials-table-wrapper {
  overflow-x: auto;
}

.credentials-table {
  width: 100%;
  border-collapse: collapse;
}

.credentials-table th {
  text-align: left;
  padding: 0.75rem 1rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e2e8f0;
}

.credentials-table td {
  padding: 1rem;
  font-size: 0.875rem;
  color: #0f172a;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.credential-row:last-child td {
  border-bottom: none;
}

.cred-name {
  font-weight: 600;
  color: #0f172a;
}

.cred-login {
  color: #64748b;
}

.cred-password {
  white-space: nowrap;
}

.password-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.password-dots {
  font-family: monospace;
  font-size: 0.875rem;
  color: #0f172a;
  letter-spacing: 0.1em;
}

.password-value {
  font-family: monospace;
  font-size: 0.875rem;
  color: #0f172a;
  word-break: break-all;
}

.btn-icon-sm {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: #f1f5f9;
  border-radius: 0.375rem;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}

.btn-icon-sm:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-icon-sm svg {
  width: 14px;
  height: 14px;
}

.cred-comment {
  color: #64748b;
  max-width: 250px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.cred-actions {
  white-space: nowrap;
}

.access-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: #f1f5f9;
  padding: 0.375rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8125rem;
  color: #64748b;
}

.access-badge svg {
  width: 14px;
  height: 14px;
}

.access-count {
  background: #e2e8f0;
  padding: 0.125rem 0.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 0.75rem;
}

.empty-credentials {
  text-align: center;
  padding: 3rem 1rem !important;
  color: #94a3b8;
}

.empty-credentials svg {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5rem;
  opacity: 0.5;
}

.empty-credentials p {
  margin: 0;
  font-size: 0.875rem;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-generate {
  background: #dcfce7;
  color: #16a34a;
}

.btn-generate:hover {
  background: #bbf7d0;
}

.btn-edit {
  background: #f1f5f9;
  color: #64748b;
}

.btn-edit:hover {
  background: #e2e8f0;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
}

.btn-delete:hover {
  background: #fee2e2;
}

.btn-secondary {
  background: #f1f5f9;
  color: #64748b;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-add-floating {
  position: absolute;
  bottom: 1.5rem;
  right: 1.5rem;
  background: #16a34a;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 6px rgba(22, 163, 74, 0.3);
}

.btn-add-floating:hover {
  background: #15803d;
  transform: translateY(-1px);
  box-shadow: 0 6px 8px rgba(22, 163, 74, 0.4);
}

.btn-add-floating svg {
  width: 16px;
  height: 16px;
}

/* Access Button in Table */
.access-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 0.5rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
  color: #16a34a;
  cursor: pointer;
  transition: all 0.2s;
}

.access-btn:hover {
  background: #dcfce7;
  border-color: #86efac;
}

.access-btn svg {
  width: 16px;
  height: 16px;
}

.access-btn .access-count {
  font-weight: 600;
}

/* Dialog Overlay */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

/* Access Dialog */
.access-dialog {
  background: white;
  border-radius: 1rem;
  width: 420px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.access-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.access-dialog-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.access-dialog-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
  margin: 0.25rem 0 0;
}

.btn-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.btn-close:hover {
  background: #f1f5f9;
  color: #64748b;
}

.btn-close svg {
  width: 20px;
  height: 20px;
}

/* Access List Section */
.access-list-section {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.access-section-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #64748b;
  margin: 0 0 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.access-loading {
  text-align: center;
  padding: 1rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.access-empty {
  text-align: center;
  padding: 1rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.access-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 240px;
  overflow-y: auto;
}

.access-user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.access-user-item:hover {
  background: #f8fafc;
}

.access-user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.access-user-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.access-user-avatar-letter {
  font-size: 0.875rem;
  font-weight: 700;
  color: white;
}

.access-user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.access-user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.access-user-login {
  font-size: 0.75rem;
  color: #94a3b8;
}

.btn-remove-access {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.btn-remove-access:hover {
  background: #fef2f2;
  color: #dc2626;
}

.btn-remove-access svg {
  width: 18px;
  height: 18px;
}

/* Add User Section */
.add-user-section {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.user-search-wrapper {
  position: relative;
}

.user-search-input {
  width: 100%;
  padding: 0.625rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.user-search-input:focus {
  border-color: #3b82f6;
}

.user-search-input::placeholder {
  color: #94a3b8;
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  margin-top: 0.25rem;
  max-height: 180px;
  overflow-y: auto;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.search-result-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  cursor: pointer;
  transition: background 0.2s;
}

.search-result-item:hover {
  background: #f8fafc;
}

.search-result-item:first-child {
  border-radius: 0.75rem 0.75rem 0 0;
}

.search-result-item:last-child {
  border-radius: 0 0 0.75rem 0.75rem;
}

.search-user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.search-user-avatar-letter {
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
}

.search-user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.search-user-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-user-login {
  font-size: 0.6875rem;
  color: #94a3b8;
}

.no-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  margin-top: 0.25rem;
  padding: 1rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.8125rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* Dialog Footer */
.access-dialog-footer {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: center;
}

.btn-close-dialog {
  width: 100%;
  background: #f1f5f9;
  color: #64748b;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-close-dialog:hover {
  background: #e2e8f0;
}

/* Add Credential Dialog */
.add-dialog {
  background: white;
  border-radius: 1rem;
  width: 480px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.add-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.add-dialog-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.add-dialog-subtitle {
  font-size: 0.8125rem;
  color: #64748b;
  margin: 0.25rem 0 0;
}

.add-dialog-body {
  padding: 1.5rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}

.form-label {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.form-input {
  width: 100%;
  padding: 0.625rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #3b82f6;
}

.form-input::placeholder {
  color: #94a3b8;
}

.password-input-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.password-input {
  flex: 1;
  font-family: monospace;
  letter-spacing: 0.05em;
}

.password-actions {
  display: flex;
  gap: 0.25rem;
}

.grant-access-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e2e8f0;
}

.grant-access-title {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #64748b;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.selected-users-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 150px;
  overflow-y: auto;
}

.selected-user-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: background 0.2s;
}

.selected-user-item:hover {
  background: #f8fafc;
}

.selected-user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.selected-user-avatar-letter {
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
}

.selected-user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.selected-user-name {
  font-size: 0.8125rem;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-remove-selected {
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s;
}

.btn-remove-selected:hover {
  background: #fef2f2;
  color: #dc2626;
}

.btn-remove-selected svg {
  width: 16px;
  height: 16px;
}

.add-dialog-footer {
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border-top: 1px solid #e2e8f0;
}

.btn-add-submit {
  width: 100%;
  background: #16a34a;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-add-submit:hover:not(:disabled) {
  background: #15803d;
}

.btn-add-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-add-submit svg {
  width: 16px;
  height: 16px;
}

.btn-cancel {
  width: 100%;
  background: #f1f5f9;
  color: #64748b;
  padding: 0.625rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel:hover {
  background: #e2e8f0;
}

/* Edit Service Dialog */
.edit-service-dialog {
  background: white;
  border-radius: 1rem;
  width: 440px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.edit-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.edit-dialog-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.edit-dialog-body {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.edit-dialog-footer {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.edit-dialog-footer .btn-secondary {
  background: #f1f5f9;
  color: #64748b;
  padding: 0.5rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.edit-dialog-footer .btn-secondary:hover {
  background: #e2e8f0;
}

.edit-dialog-footer .btn-primary {
  background: #0f172a;
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.edit-dialog-footer .btn-primary:hover:not(:disabled) {
  background: #1e293b;
}

.edit-dialog-footer .btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .service-info-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .service-info-actions {
    width: 100%;
    flex-wrap: wrap;
  }

  .stats-row {
    grid-template-columns: 1fr;
  }

  .credentials-table th,
  .credentials-table td {
    padding: 0.75rem 0.5rem;
  }

  .cred-comment {
    max-width: 120px;
  }

  .access-dialog {
    width: 90vw;
    max-width: 420px;
  }
}
</style>
