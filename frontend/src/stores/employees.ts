import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'

interface Employee {
  user_id: number
  full_name: string | null
  login: string | null
  phone: string | null
  avatar_url: string | null
  role: string | null
  status: string | null
  access_count: number
}

interface CreateEmployeeData {
  full_name: string
  login: string
  password: string
  phone?: string
  avatar_url?: string
  role?: string
  status?: string
}

export const useEmployeesStore = defineStore('employees', () => {
  const authStore = useAuthStore()

  const employees = ref<Employee[]>([])
  const loading = ref(false)
  const searchQuery = ref('')
  const statusFilter = ref('')

  const filteredEmployees = computed(() => {
    let result = employees.value

    if (statusFilter.value) {
      result = result.filter((e) => e.status === statusFilter.value)
    }

    if (searchQuery.value) {
      const q = searchQuery.value.toLowerCase()
      result = result.filter(
        (e) =>
          (e.full_name ?? '').toLowerCase().includes(q) ||
          (e.login ?? '').toLowerCase().includes(q) ||
          (e.phone ?? '').toLowerCase().includes(q)
      )
    }

    return result
  })

  const totalCount = computed(() => employees.value.length)
  const activeCount = computed(() => employees.value.filter((e) => e.status === 'active').length)
  const blockedCount = computed(() => employees.value.filter((e) => e.status === 'blocked').length)

  async function fetchEmployees() {
    if (!authStore.token) return
    loading.value = true
    try {
      const params = new URLSearchParams()
      if (searchQuery.value) params.set('search', searchQuery.value)
      if (statusFilter.value) params.set('status_filter', statusFilter.value)

      const response = await fetch(`/api/users/?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        employees.value = await response.json()
      }
    } finally {
      loading.value = false
    }
  }

  async function createEmployee(data: CreateEmployeeData) {
    if (!authStore.token) return null
    try {
      const response = await fetch('/api/users/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      if (response.ok) {
        const created = await response.json()
        employees.value.push(created)
        return created
      }
      return null
    } catch {
      return null
    }
  }

  async function updateStatus(user_id: number, status: string) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${user_id}/status`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
      })
      if (response.ok) {
        const emp = employees.value.find((e) => e.user_id === user_id)
        if (emp) emp.status = status
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function deleteEmployee(user_id: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${user_id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        employees.value = employees.value.filter((e) => e.user_id !== user_id)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  return {
    employees,
    loading,
    searchQuery,
    statusFilter,
    filteredEmployees,
    totalCount,
    activeCount,
    blockedCount,
    fetchEmployees,
    createEmployee,
    updateStatus,
    deleteEmployee,
  }
})
