import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

interface UserWithAccess {
    user_id: number
    full_name: string | null
    login: string | null
    avatar_url: string | null
    role: string | null
    status: string | null
}

export const useAccessStore = defineStore('access', () => {
    const authStore = useAuthStore()

    const usersWithAccess = ref<UserWithAccess[]>([])
    const searchResults = ref<UserWithAccess[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function fetchUsersWithAccess(serviceId: number, credentialId: number) {
        if (!authStore.token) return
        loading.value = true
        error.value = null
        try {
            const response = await fetch(
                `/api/services/${serviceId}/credentials/${credentialId}/access`,
                {
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                }
            )
            if (response.ok) {
                usersWithAccess.value = await response.json()
            } else {
                error.value = 'Не вдалося завантажити список доступу'
            }
        } catch {
            error.value = "Помилка з'єднання з сервером"
        } finally {
            loading.value = false
        }
    }

    async function searchUsers(searchQuery: string) {
        if (!authStore.token) return
        try {
            const response = await fetch(
                `/api/users/?search=${encodeURIComponent(searchQuery)}`,
                {
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                }
            )
            if (response.ok) {
                const allUsers = await response.json()
                // Фільтруємо тих, хто вже має доступ
                const userIdsWithAccess = new Set(usersWithAccess.value.map(u => u.user_id))
                searchResults.value = allUsers.filter((u: UserWithAccess) => !userIdsWithAccess.has(u.user_id))
            }
        } catch {
            // Ігноруємо помилки пошуку
        }
    }

    async function grantAccess(serviceId: number, credentialId: number, userId: number) {
        if (!authStore.token) return false
        try {
            const response = await fetch(
                `/api/services/${serviceId}/credentials/${credentialId}/access`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ user_id: userId })
                }
            )
            if (response.ok) {
                // Оновлюємо список доступу
                await fetchUsersWithAccess(serviceId, credentialId)
                return true
            } else {
                const err = await response.json().catch(() => ({}))
                error.value = err.detail || 'Не вдалося надати доступ'
                return false
            }
        } catch {
            error.value = "Помилка з'єднання з сервером"
            return false
        }
    }

    async function revokeAccess(serviceId: number, credentialId: number, userId: number) {
        if (!authStore.token) return false
        try {
            const response = await fetch(
                `/api/services/${serviceId}/credentials/${credentialId}/access/${userId}`,
                {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`
                    }
                }
            )
            if (response.ok) {
                // Оновлюємо список доступу
                await fetchUsersWithAccess(serviceId, credentialId)
                return true
            } else {
                error.value = 'Не вдалося забрати доступ'
                return false
            }
        } catch {
            error.value = "Помилка з'єднання з сервером"
            return false
        }
    }

    function clearAccess() {
        usersWithAccess.value = []
        searchResults.value = []
        error.value = null
    }

    return {
        usersWithAccess,
        searchResults,
        loading,
        error,
        fetchUsersWithAccess,
        searchUsers,
        grantAccess,
        revokeAccess,
        clearAccess,
    }
})
