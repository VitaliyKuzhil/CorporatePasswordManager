import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MyAccessView from '../views/MyAccessView.vue'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import UsersView from '../views/UsersView.vue'
import ServiceDetailView from '../views/ServiceDetailView.vue'
import EmployeeDetailView from '../views/EmployeeDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MyAccessView,
      meta: { requiresAuth: true }
    },
    {
      path: '/services',
      name: 'services',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView,
      meta: { requiresAuth: true }
    },
    {
      path: '/service/:id',
      name: 'serviceDetail',
      component: ServiceDetailView,
      meta: { requiresAuth: true }
    },
    {
      path: '/employee/:id',
      name: 'employeeDetail',
      component: EmployeeDetailView,
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Валідуємо токен перед перевіркою авторизації
  await authStore.validateToken()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Якщо маршрут потребує авторизації і користувач не залогінений
    next({ name: 'login' })
    return
  }

  if (to.name === 'login' && authStore.isAuthenticated) {
    // Якщо користувач вже залогінений і намагається зайти на сторінку логіна
    // Адміни йдуть на Список джерел, решта — на Мої доступи
    if (authStore.user?.role === 'admin') {
      next({ name: 'services' })
    } else {
      next({ name: 'home' })
    }
    return
  }

  // Якщо адмін потрапляє на / (Мої доступи), перенаправляємо на /services
  if (to.name === 'home' && authStore.user?.role === 'admin') {
    next({ name: 'services' })
    return
  }

  next()
})

export default router
