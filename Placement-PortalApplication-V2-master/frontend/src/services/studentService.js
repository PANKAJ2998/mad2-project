import api from './api'

export default {
  getProfile() {
    return api.get('/student/profile')
  },

  updateProfile(data) {
    return api.put('/student/profile', data)
  }
}
