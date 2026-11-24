import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './auth'

interface CredentialCreateData {
    login: string
    password: string
    comment: string
    user_ids: number[]
}

interface CredentialUpdateData {
    login?: string | null
    password?: string | null
    totp_secret?: string | null
    comment?: string | null
    user_ids?: number[] | null
}

export const useCredentialsStore = defineStore('credentials', () => {
    const authStore = useAuthStore()

    const loading = ref(false)
    const error = ref<string | null>(null)

    async function createCredential(serviceId: number, data: CredentialCreateData) {
        if (!authStore.token) return null
        loading.value = true
        error.value = null
        try {
            const response = await fetch(
                `/api/services/${serviceId}/credentials`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        login: data.login || null,
                        password: data.password,
                        comment: data.comment || null,
                        user_ids: data.user_ids
                    })
                }
            )
            if (response.ok) {
                const result = await response.json()
                return result
            } else {
                const err = await response.json().catch(() => ({}))
                error.value = err.detail || 'Не вдалося створити пароль'
                return null
            }
        } catch {
            error.value = "Помилка з'єднання з сервером"
            return null
        } finally {
            loading.value = false
        }
    }

    async function updateCredential(serviceId: number, credentialId: number, data: CredentialUpdateData) {
        if (!authStore.token) return null
        loading.value = true
        error.value = null
        try {
            const response = await fetch(
                `/api/services/${serviceId}/credentials/${credentialId}`,
                {
                    method: 'PUT',
                    headers: {
                        'Authorization': `Bearer ${authStore.token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }
            )
            if (response.ok) {
                const result = await response.json()
                return result
            } else {
                const err = await response.json().catch(() => ({}))
                error.value = err.detail || 'Не вдалося оновити пароль'
                return null
            }
        } catch {
            error.value = "Помилка з'єднання з сервером"
            return null
        } finally {
            loading.value = false
        }
    }

    function clearError() {
        error.value = null
    }

    return {
        loading,
        error,
        createCredential,
        updateCredential,
        clearError,
    }
})
