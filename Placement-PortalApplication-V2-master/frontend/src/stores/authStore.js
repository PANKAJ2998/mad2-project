import { defineStore } from 'pinia'
import authService from '@/services/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: authService.getUser(),
    token: authService.getToken(),
    role: authService.getRole(),
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
    isCompany: (state) => state.role === 'company',
    isStudent: (state) => state.role === 'student'
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await authService.login(credentials)
        if (response.data.success) {
          const { token, user } = response.data.data
          this.token = token
          this.user = user
          this.role = user.role

          localStorage.setItem('token', token)
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('role', user.role)

          return true
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async registerStudent(data) {
      this.loading = true
      this.error = null
      try {
        const response = await authService.registerStudent(data)
        if (response.data.success) {
          const { token, user } = response.data.data
          this.token = token
          this.user = user
          this.role = user.role

          localStorage.setItem('token', token)
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('role', user.role)

          return true
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async registerCompany(data) {
      this.loading = true
      this.error = null
      try {
        const response = await authService.registerCompany(data)
        if (response.data.success) {
          const { token, user } = response.data.data
          this.token = token
          this.user = user
          this.role = user.role

          localStorage.setItem('token', token)
          localStorage.setItem('user', JSON.stringify(user))
          localStorage.setItem('role', user.role)

          return true
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.role = null
      authService.logout()
    }
  }
})
