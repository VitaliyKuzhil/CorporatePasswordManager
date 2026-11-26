import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

interface EmployeeDetail {
  user_id: number
  full_name: string | null
  login: string | null
  phone: string | null
  avatar_url: string | null
  role: string | null
  status: string | null
  access_count: number
}

interface EmployeeCredential {
  credential_id: number
  service_id: number
  service_name: string
  service_url: string | null
  service_logo_url: string | null
  login: string
  password: string
  comment: string | null
  showPassword?: boolean
}

export const useEmployeeDetailStore = defineStore('employeeDetail', () => {
  const authStore = useAuthStore()

  const employee = ref<EmployeeDetail | null>(null)
  const credentials = ref<EmployeeCredential[]>([])
  const loading = ref(false)

  async function fetchEmployee(user_id: number) {
    if (!authStore.token) return
    loading.value = true
    try {
      const response = await fetch(`/api/users/${user_id}`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        employee.value = await response.json()
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchCredentials(user_id: number) {
    if (!authStore.token) return
    loading.value = true
    try {
      const response = await fetch(`/api/users/${user_id}/credentials`, {
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        credentials.value = await response.json()
      }
    } finally {
      loading.value = false
    }
  }

  async function fetchLoginPassword(user_id: number) {
    if (!authStore.token) return null
    try {
      const response = await fetch(`/api/users/${user_id}/login-password`, {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      })
      if (!response.ok) return null
      return await response.json() as { login: string; password: string }
    } catch {
      return null
    }
  }

  async function grantCredential(user_id: number, credential_id: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${user_id}/credentials`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ credential_id })
      })
      if (response.ok) {
        // Оновлюємо список креденшалів
        await fetchCredentials(user_id)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function revokeCredential(user_id: number, credential_id: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${user_id}/credentials/${credential_id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.token}`
        }
      })
      if (response.ok) {
        await fetchCredentials(user_id)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function grantAllCredentialsToUser(targetUserId: number, sourceUserId: number) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${targetUserId}/grant-all-credentials`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ source_user_id: sourceUserId })
      })
      if (response.ok) {
        await fetchCredentials(targetUserId)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  async function updateEmployee(user_id: number, data: { full_name?: string; phone?: string; login?: string; password?: string }) {
    if (!authStore.token) return false
    try {
      const response = await fetch(`/api/users/${user_id}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${authStore.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      if (response.ok) {
        // Оновлюємо дані працівника
        await fetchEmployee(user_id)
        return true
      }
      return false
    } catch {
      return false
    }
  }

  function clear() {
    employee.value = null
    credentials.value = []
  }

  return {
    employee,
    credentials,
    loading,
    fetchEmployee,
    fetchCredentials,
    fetchLoginPassword,
    grantCredential,
    revokeCredential,
    grantAllCredentialsToUser,
    updateEmployee,
    clear
  }
})
