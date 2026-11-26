import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export interface MyAccessCredential {
  credential_id: number
  login: string | null
  comment: string | null
}

export interface MyAccessService {
  service_id: number
  service_name: string
  service_url: string | null
  service_logo_url: string | null
  auth_type: 'password_2fa' | 'sso_link'
  credentials: MyAccessCredential[]
}

export const useMyAccessStore = defineStore('myAccess', () => {
  const authStore = useAuthStore()
  const services = ref<MyAccessService[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const searchQuery = ref('')

  const filteredServices = computed(() => {
    if (!searchQuery.value.trim()) return services.value

    const q = searchQuery.value.toLowerCase().trim()
    return services.value.filter((service) => {
      const serviceMatch = service.service_name.toLowerCase().includes(q)
      const urlMatch = service.service_url?.toLowerCase().includes(q) || false
      const credMatch = service.credentials.some((c) =>
        c.login?.toLowerCase().includes(q) ||
        c.comment?.toLowerCase().includes(q)
      )
      return serviceMatch || urlMatch || credMatch
    })
  })

  const totalCredentials = computed(() => {
    return filteredServices.value.reduce((sum, s) => sum + s.credentials.length, 0)
  })

  async function fetchMyAccess() {
    if (!authStore.token) return
    loading.value = true
    error.value = null
    try {
      const response = await fetch('/api/services/my-access', {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        services.value = await response.json()
      } else {
        error.value = 'Не вдалося завантажити список доступів'
      }
    } catch {
      error.value = 'Помилка підключення до сервера'
    } finally {
      loading.value = false
    }
  }

  return { services, loading, error, searchQuery, filteredServices, totalCredentials, fetchMyAccess }
})
