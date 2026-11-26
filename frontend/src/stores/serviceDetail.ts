import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

interface CredentialItem {
  credential_id: number
  login: string | null
  password: string | null
  totp_secret: string | null
  comment: string | null
  access_count: number
}

interface ServiceDetail {
  service_id: number
  service_name: string
  service_url: string | null
  service_logo_url: string | null
  credential_count: number
  access_count: number
  auth_type: 'password_2fa' | 'sso_link'
  credentials: CredentialItem[]
}

export const useServiceDetailStore = defineStore('serviceDetail', () => {
  const authStore = useAuthStore()

  const detail = ref<ServiceDetail | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchServiceDetail(serviceId: number) {
    if (!authStore.token) return
    loading.value = true
    error.value = null
    try {
      const response = await fetch(`/api/services/${serviceId}/detail`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        detail.value = await response.json()
      } else {
        error.value = 'Не вдалося завантажити деталі сервісу'
      }
    } catch {
      error.value = 'Помилка з\'єднання з сервером'
    } finally {
      loading.value = false
    }
  }

  async function deleteCredential(serviceId: number, credentialId: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/services/${serviceId}/credentials/${credentialId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      return response.ok
    } catch {
      return false
    }
  }

  function clearDetail() {
    detail.value = null
    error.value = null
  }

  return {
    detail,
    loading,
    error,
    fetchServiceDetail,
    deleteCredential,
    clearDetail,
  }
})
