import api from './api'

export default {
  getStudentDrives() {
    return api.get('/student/drives')
  },

  getCompanyDrives() {
    return api.get('/company/my-drives')
  },

  getAllDrives() {
    return api.get('/admin/drives')
  },

  createDrive(data) {
    return api.post('/company/create-drive', data)
  },

  updateDrive(driveId, data, isAdmin = false) {
    const endpoint = isAdmin ? `/admin/drive/${driveId}` : `/company/drive/${driveId}`
    return api.put(endpoint, data)
  },

  deleteDrive(driveId, isAdmin = false) {
    const endpoint = isAdmin ? `/admin/drive/${driveId}` : `/company/drive/${driveId}`
    return api.delete(endpoint)
  },

  approveDrive(driveId) {
    return api.post(`/admin/approve-drive/${driveId}`)
  },

  getDriveApplications(driveId) {
    return api.get(`/company/drive-applications/${driveId}`)
  }
}
