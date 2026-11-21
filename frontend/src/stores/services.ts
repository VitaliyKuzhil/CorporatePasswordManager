import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

interface Service {
  service_id: number
  service_name: string
  service_url: string | null
  service_logo_url: string | null
  credential_count: number
}

interface ServiceCreateData {
  service_name: string
  service_url?: string
  service_logo_url?: string
}

interface ServiceUpdateData {
  service_name?: string
  service_url?: string
  service_logo_url?: string
}

export const useServicesStore = defineStore('services', () => {
  const authStore = useAuthStore()

  const services = ref<Service[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const searchQuery = ref('')
  const filterSource = ref('')

  const filteredServices = computed(() => {
    let result = services.value

    // Фільтр за пошуком (пошук по назві та URL)
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(s =>
        s.service_name.toLowerCase().includes(query) ||
        (s.service_url && s.service_url.toLowerCase().includes(query))
      )
    }

    // Фільтр за конкретним джерелом
    if (filterSource.value) {
      result = result.filter(s => s.service_id.toString() === filterSource.value)
    }

    return result
  })

  const totalPasswords = computed(() => {
    return filteredServices.value.reduce((sum, s) => sum + s.credential_count, 0)
  })

  const totalSources = computed(() => filteredServices.value.length)

  const uniqueSourceNames = computed(() => {
    return services.value.map(s => ({ id: s.service_id.toString(), name: s.service_name }))
  })

  async function fetchServices() {
    if (!authStore.token) return
    loading.value = true
    error.value = null
    try {
      const response = await fetch('/api/services/', {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        services.value = await response.json()
      } else {
        error.value = 'Не вдалося завантажити список джерел'
      }
    } catch {
      error.value = 'Помилка з\'єднання з сервером'
    } finally {
      loading.value = false
    }
  }

  async function createService(data: ServiceCreateData) {
    if (!authStore.token) return false
    try {
      const response = await fetch('/api/services/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      if (response.ok) {
        await fetchServices()
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function updateService(id: number, data: ServiceUpdateData) {
    if (!authStore.token) return false
    try {
      // Перетворюємо порожні рядки в undefined, щоб бекенд не оновлював ці поля
      const cleanData: ServiceUpdateData = {}
      if (data.service_name !== undefined && data.service_name !== '') {
        cleanData.service_name = data.service_name
      }
      if (data.service_url !== undefined && data.service_url !== '') {
        cleanData.service_url = data.service_url
      }
      if (data.service_logo_url !== undefined && data.service_logo_url !== '') {
        cleanData.service_logo_url = data.service_logo_url
      }
      const response = await fetch(`/api/services/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(cleanData)
      })
      if (response.ok) {
        await fetchServices()
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function deleteService(id: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/services/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        await fetchServices()
        return true
      }
      return false
    } catch {
      return false
    }
  }

  return {
    services,
    loading,
    error,
    searchQuery,
    filterSource,
    filteredServices,
    totalPasswords,
    totalSources,
    uniqueSourceNames,
    fetchServices,
    createService,
    updateService,
    deleteService,
  }
})
