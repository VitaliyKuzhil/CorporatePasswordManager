import { defineStore } from 'pinia'
import { ref } from 'vue'

interface UserProfile {
  id: number
  login: string
  full_name: string | null
  phone: string | null
  avatar_url: string | null
  role: string
  status: string | null
}

interface UpdateProfileData {
  full_name?: string
  phone?: string
  avatar_url?: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<UserProfile | null>(null)
  const error = ref<string | null>(null)
  const isAuthenticated = ref<boolean>(false)
  const tokenValidated = ref<boolean>(false)

  async function validateToken() {
    if (tokenValidated.value) return
    tokenValidated.value = true
    if (!token.value) {
      isAuthenticated.value = false
      return
    }
    try {
      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      if (response.ok) {
        user.value = await response.json()
        isAuthenticated.value = true
      } else {
        // Токен невалідний, видаляємо його
        token.value = null
        user.value = null
        isAuthenticated.value = false
        localStorage.removeItem('token')
      }
    } catch {
      // Помилка підключення, залишаємо токен для повторної спроби
      isAuthenticated.value = false
    }
  }

  async function login(username: string, password: string) {
    error.value = null
    try {
      // FastAPI OAuth2 очікує form-data, а не JSON
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)

      // Завдяки vite.config.ts, '/api' автоматично проксіюється на бекенд
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Неправильний логін або пароль')
      }

      const data = await response.json()
      token.value = data.access_token
      isAuthenticated.value = true
      localStorage.setItem('token', data.access_token)

      // Отримати профіль користувача після успішного входу
      await fetchProfile()

      return true
    } catch (e: any) {
      error.value = e.message
      return false
    }
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      if (response.ok) {
        user.value = await response.json()
      }
    } catch {
      // Ігнорувати помилки при отриманні профілю
    }
  }

  async function updateProfile(data: UpdateProfileData) {
    if (!token.value || !user.value) return false
    try {
      const response = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      if (response.ok) {
        const updated = await response.json()
        user.value = updated
        return true
      }
      return false
    } catch {
      return false
    }
  }

  function logout() {
    token.value = null
    user.value = null
    isAuthenticated.value = false
    tokenValidated.value = false
    localStorage.removeItem('token')
  }

  return { token, user, isAuthenticated, error, login, logout, fetchProfile, updateProfile, validateToken }
})