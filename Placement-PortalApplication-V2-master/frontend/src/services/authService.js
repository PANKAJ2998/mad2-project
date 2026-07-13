import api from './api'

export default {
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  registerStudent(data) {
    return api.post('/auth/register/student', data)
  },

  registerCompany(data) {
    return api.post('/auth/register/company', data)
  },

  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('role')
  },

  getToken() {
    return localStorage.getItem('token')
  },

  getUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  getRole() {
    return localStorage.getItem('role')
  },

  isAuthenticated() {
    return !!this.getToken()
  }
}
