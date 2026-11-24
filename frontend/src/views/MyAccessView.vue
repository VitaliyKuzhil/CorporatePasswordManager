<template>
  <div class="my-access-page">
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h1 class="page-title">Мої доступи</h1>
        <p class="page-subtitle">Сервіси, до яких адміністратор надав вам доступ</p>
      </div>
      <div class="session-info" v-if="authStore.user">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2v10M12 18h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Сесія ще {{ sessionRemaining }}</span>
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

      <div class="filter-select-wrapper">
        <select
          v-model="filterAuthType"
          class="filter-select"
        >
          <option value="">Усі типи входу</option>
          <option value="password_2fa">Пароль + 2FA</option>
          <option value="sso_link">SSO — вхід за посиланням</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="loading-state">
      <div class="spinner"></div>
      <p>Завантаження...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="filteredServices.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 11H5M19 11C20.1046 11 21 11.8954 21 13V19C21 20.1046 20.1046 21 19 21H5C3.89543 21 3 20.1046 3 19V13C3 11.8954 3.89543 11 5 11M19 11V9C20.1046 9 21 8.10457 21 7V5C21 3.89543 20.1046 3 19 3H5C3.89543 3 3 3.89543 3 5V7C3 8.10457 3.89543 9 5 9V11M19 11H5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <p>Доступи не знайдено</p>
      <p class="empty-hint">Зверніться до адміністратора для надання доступу</p>
    </div>

    <!-- Services Content -->
    <template v-else>
      <!-- External Services Section (password_2fa) -->
      <div v-if="externalServices.length > 0" class="services-section">
        <div class="section-header">
          <h2 class="section-title">Зовнішні сервіси</h2>
          <div class="section-badge">Пароль + 2FA</div>
          <p class="section-hint">Скопіюйте логін / пароль, натисніть «Увійти» — з'явиться 2FA-код</p>
        </div>

        <div class="services-grid">
          <div
            v-for="(service, sIndex) in externalServices"
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
                  {{ getServiceDomain(service.service_url) }}
                </a>
              </div>
            </div>

            <!-- Credentials -->
            <div class="credentials-list">
              <div
                v-for="cred in service.credentials"
                :key="cred.credential_id"
                class="credential-row"
              >
                <!-- Login Field -->
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

                <!-- Password Field -->
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

                <!-- 2FA Code Field -->
                <div class="credential-field totp-field" v-if="cred.totp_secret">
                  <label class="field-label">
                    2FA
                    <span v-if="totpTimers.has(cred.credential_id)" class="totp-timer">{{ totpTimers.get(cred.credential_id) }} с</span>
                  </label>
                  <div class="field-value-wrapper totp-wrapper">
                    <span class="field-value totp-code">{{ getTOTPCode(cred.credential_id) }}</span>
                    <button class="btn-icon btn-copy" @click="copyTOTPCode(cred.credential_id)" title="Копіювати 2FA-код">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M8 4V16C8 17.1046 8.89543 18 10 18H18C19.1046 18 20 17.1046 20 16V4C20 2.89543 19.1046 2 18 2H10C8.89543 2 8 2.89543 8 4ZM16 18V20C16 21.1046 15.1046 22 14 22H4C2.89543 22 2 21.1046 2 20V8C2 6.89543 2.89543 6 4 6H10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                    </button>
                  </div>
                </div>
                <div v-else class="credential-field totp-field totp-placeholder">
                  <label class="field-label">2FA</label>
                  <div class="field-value-wrapper totp-placeholder-wrapper">
                    <span class="field-value totp-placeholder-text">Код з'явиться після натискання «Увійти»</span>
                  </div>
                </div>

                <!-- Login Button -->
                <button
                  class="btn-login"
                  @click="handleLogin(service, cred)"
                >
                  Увійти
                  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5 12H19M19 12H13M19 12L15 8M19 12L15 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Corporate Services Section (sso_link) -->
      <div v-if="ssoServices.length > 0" class="services-section">
        <div class="section-header">
          <h2 class="section-title">Корпоративні сервіси</h2>
          <div class="section-badge sso">SSO — вхід по кнопці</div>
          <p class="section-hint">Вхід одним натисканням</p>
        </div>

        <div class="services-grid">
          <div
            v-for="(service, sIndex) in ssoServices"
            :key="service.service_id"
            class="service-card sso-card"
          >
            <!-- Service Header -->
            <div class="service-header">
              <div class="service-icon" :style="{ backgroundColor: getSsoServiceColor(sIndex) }">
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
                  {{ getServiceDomain(service.service_url) }}
                </a>
              </div>
            </div>

            <!-- SSO Info -->
            <div class="sso-info">
              <p class="sso-description">Пароль не потрібен: система авторизує вас автоматично.</p>
              <button
                class="btn-login"
                @click="handleSsoLogin(service)"
              >
                Увійти
                <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 12H19M19 12H13M19 12L15 8M19 12L15 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- Toast notification -->
    <div v-if="toastMessage" class="toast">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useMyAccessStore } from '@/stores/myAccess'
import { useAuthStore } from '@/stores/auth'

const store = useMyAccessStore()
const authStore = useAuthStore()
const filterService = ref<number | ''>('')
const filterAuthType = ref<'password_2fa' | 'sso_link' | ''>('')
const passwordVisibility = ref(new Set<number>())
const avatarErrors = ref(new Set<number>())
const toastMessage = ref('')
let toastTimer: ReturnType<typeof setTimeout> | null = null

// TOTP state
const totpCodes = ref<Record<number, string>>({})
const totpTimers = ref<Map<number, number>>(new Map())
let totpInterval: ReturnType<typeof setInterval> | null = null

// Session timer
const sessionRemaining = ref('12 год 0 хв')

// TOTP via Web Crypto API
async function generateTOTP(secret: string): Promise<string> {
  try {
    // Decode base32 secret to bytes
    let cleanSecret = secret.replace(/\s+/g, '').toUpperCase()
    // Pad short secrets (e.g., from Notion: 16 chars = 80 bits) to 24 chars (120 bits) for Web Crypto
    if (cleanSecret.length < 24) {
      cleanSecret = cleanSecret.padEnd(24, 'A')
    }
    const key = urlBase32ToUint8Array(cleanSecret)

    // Get current time step (30 second period)
    const now = Math.floor(Date.now() / 1000)
    const timeStep = Math.floor(now / 30)
    const timeHex = BigInt(timeStep).toString(16).padStart(16, '0')
    const timeBytes = new Uint8Array(8)
    for (let i = 0; i < 8; i++) {
      timeBytes[i] = parseInt(timeHex.substr(i * 2, 2), 16)
    }

    // Import key and sign
    const cryptoKey = await crypto.subtle.importKey(
      'raw',
      key.buffer as ArrayBuffer,
      { name: 'HMAC', hash: 'SHA-1' },
      false,
      ['sign']
    )
    const sig = await crypto.subtle.sign('HMAC', cryptoKey, timeBytes)
    const hmac = new Uint8Array(sig)

    // Dynamic truncation
    const offset = hmac[hmac.length - 1]! & 0x0f
    const b0 = hmac[offset] ?? 0
    const b1 = hmac[offset + 1] ?? 0
    const b2 = hmac[offset + 2] ?? 0
    const b3 = hmac[offset + 3] ?? 0
    const code = ((b0 & 0x7f) << 24 | (b1 & 0xff) << 16 | (b2 & 0xff) << 8 | (b3 & 0xff)) % 1000000

    return String(code).padStart(6, '0')
  } catch (e) {
    console.error('TOTP generation failed:', e)
    return '000000'
  }
}

function urlBase32ToUint8Array(base32: string): Uint8Array {
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
  const buffer: number[] = []
  let bits = 0
  let value = 0

  for (let i = 0; i < base32.length; i++) {
    const char = base32[i]
    if (!char) continue
    const idx = alphabet.indexOf(char)
    if (idx === -1) continue
    value = (value << 5) | idx
    bits += 5
    if (bits >= 8) {
      bits -= 8
      buffer.push((value >> bits) & 0xff)
    }
  }

  return new Uint8Array(buffer)
}

// Filtered services
const filteredServices = computed(() => {
  let result = store.filteredServices
  if (filterService.value !== '') {
    result = result.filter(s => s.service_id === filterService.value)
  }
  if (filterAuthType.value !== '') {
    result = result.filter(s => s.auth_type === filterAuthType.value)
  }
  return result
})

// Split by auth type
const externalServices = computed(() => {
  return filteredServices.value.filter(s => s.auth_type === 'password_2fa')
})

const ssoServices = computed(() => {
  return filteredServices.value.filter(s => s.auth_type === 'sso_link')
})

const serviceColors = [
  '#EA4335', '#333', '#5865F2', '#0052CC', '#FF6600',
  '#0078D4', '#4285F4', '#1DA1F2', '#000', '#7B68EE'
]

const ssoServiceColors = [
  '#059669', '#7C3AED', '#2563EB', '#DC2626', '#D97706'
]

function getServiceColor(index: number): string {
  return serviceColors[index % serviceColors.length] || '#EA4335'
}

function getSsoServiceColor(index: number): string {
  return ssoServiceColors[index % ssoServiceColors.length] || '#059669'
}

function getInitials(name: string | undefined): string {
  return (name || '?').charAt(0).toUpperCase()
}

function getServiceDomain(url: string | null | undefined): string {
  if (!url) return '—'
  try {
    const parsed = new URL(url)
    return parsed.hostname.replace('www.', '')
  } catch {
    return url
  }
}

function handleAvatarError(event: Event, service: any) {
  avatarErrors.value.add(service.service_id)
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
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

// TOTP functions
function getTOTPCode(credentialId: number): string {
  const code = totpCodes.value[credentialId]
  if (!code) return '—— ———'
  // Format as "482 910"
  return code.replace(/(\d{3})(\d{3})/, '$1 $2')
}

async function updateTOTPCodes() {
  const updatedCodes: Record<number, string> = {}
  const updatedTimers = new Map<number, number>()
  const now = Math.floor(Date.now() / 1000)
  const timeRemaining = 30 - (now % 30)

  for (const service of externalServices.value) {
    for (const cred of service.credentials) {
      if (cred.totp_secret) {
        try {
          updatedCodes[cred.credential_id] = await generateTOTP(cred.totp_secret)
        } catch {
          updatedCodes[cred.credential_id] = '000000'
        }
        updatedTimers.set(cred.credential_id, timeRemaining)
      }
    }
  }

  totpCodes.value = updatedCodes
  totpTimers.value = updatedTimers
}

function copyToClipboard(text: string) {
  if (!text) return
  navigator.clipboard.writeText(text).then(() => {
    showToast('Скопійовано в буфер обміну')
  })
}

function copyTOTPCode(credentialId: number) {
  const code = totpCodes.value[credentialId]
  if (code) {
    navigator.clipboard.writeText(code).then(() => {
      showToast('2FA-код скопійовано')
    })
  }
}

function showToast(message: string) {
  toastMessage.value = message
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ''
  }, 2000)
}

async function handleLogin(service: any, cred: any) {
  // If there's a TOTP secret, generate the code on login
  if (cred.totp_secret) {
    try {
      const code = await generateTOTP(cred.totp_secret)
      totpCodes.value[cred.credential_id] = code
      const now = Math.floor(Date.now() / 1000)
      totpTimers.value.set(cred.credential_id, 30 - (now % 30))
    } catch (e) {
      console.error('TOTP generation failed:', e)
    }
  }

  // Open the service URL in a new tab
  if (service.service_url) {
    window.open(service.service_url, '_blank', 'noopener,noreferrer')
  }
}

async function handleSsoLogin(service: any) {
  try {
    const token = authStore.token
    if (!token) return

    // Get the first credential ID for this service
    const credId = service.credentials[0]?.credential_id
    if (!credId) {
      // Fallback: open service URL directly
      if (service.service_url) {
        window.open(service.service_url, '_blank', 'noopener,noreferrer')
      }
      return
    }

    const response = await fetch(`/api/services/credentials/${credId}/access-data`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const data = await response.json()
      if (data.strategy === 'sso_link' && data.redirect_url) {
        window.open(data.redirect_url, '_blank', 'noopener,noreferrer')
      } else if (data.url) {
        window.open(data.url, '_blank', 'noopener,noreferrer')
      }
    }
  } catch (e) {
    console.error('SSO login failed:', e)
    // Fallback: open service URL
    if (service.service_url) {
      window.open(service.service_url, '_blank', 'noopener,noreferrer')
    }
  }
}

onMounted(() => {
  store.fetchMyAccess()
  // Update TOTP codes every second
  totpInterval = setInterval(updateTOTPCodes, 1000)
  updateTOTPCodes()
})

onUnmounted(() => {
  if (totpInterval) clearInterval(totpInterval)
  if (toastTimer) clearTimeout(toastTimer)
})

// Reset TOTP codes when filters change
watch([filteredServices], () => {
  updateTOTPCodes()
})
</script>

<style scoped>
.my-access-page {
  width: 100%;
  padding-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 0.5rem;
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

.session-info {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  font-size: 0.8125rem;
  color: #64748b;
  white-space: nowrap;
}

.session-info svg {
  width: 16px;
  height: 16px;
}

/* Filter Block */
.filter-block {
  display: flex;
  align-items: center;
  gap: 0.75rem;
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
  border-color: #059669;
  background: white;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
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
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
}

.filter-select:focus {
  border-color: #059669;
  background-color: white;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

/* Services Section */
.services-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.section-title {
  font-size: 0.9375rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.section-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  background: #ecfdf5;
  color: #059669;
  border-radius: 9999px;
  font-size: 0.6875rem;
  font-weight: 600;
}

.section-badge.sso {
  background: #eff6ff;
  color: #2563eb;
}

.section-hint {
  font-size: 0.75rem;
  color: #94a3b8;
  margin: 0;
  margin-left: auto;
}

/* Services Grid */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
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
  display: flex;
  flex-direction: column;
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
  gap: 0.75rem;
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
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.totp-timer {
  background: #fef3c7;
  color: #d97706;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: none;
  letter-spacing: normal;
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

/* TOTP Field */
.totp-field {
  /* default styles */
}

.totp-wrapper {
  background: #faf5ff;
  border-color: #e9d5ff;
}

.totp-code {
  font-size: 1rem !important;
  font-weight: 700;
  color: #7c3aed;
  letter-spacing: 0.05em;
}

.totp-placeholder {
  /* placeholder styles */
}

.totp-placeholder-wrapper {
  background: #f8fafc;
  border-color: #e2e8f0;
  border-style: dashed;
}

.totp-placeholder-text {
  font-size: 0.75rem !important;
  color: #94a3b8;
  font-family: inherit !important;
  font-style: italic;
}

/* Login Button */
.btn-login {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: #059669;
  border: none;
  border-radius: 0.75rem;
  font-size: 0.8125rem;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.25rem;
}

.btn-login:hover {
  background: #047857;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.3);
}

.btn-login svg {
  width: 16px;
  height: 16px;
}

/* SSO Card */
.sso-card .sso-info {
  padding: 1rem 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sso-description {
  font-size: 0.8125rem;
  color: #64748b;
  margin: 0;
  line-height: 1.5;
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

/* Loading & Empty States */
.loading-state,
.empty-state {
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
  border-top-color: #059669;
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

  .page-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .section-hint {
    margin-left: 0;
  }
}
</style>
