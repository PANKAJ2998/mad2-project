import api from './api'

export default {
  applyToDrive(driveId) {
    return api.post(`/student/apply-drive/${driveId}`)
  },

  getMyApplications() {
    return api.get('/student/my-applications')
  },

  updateApplicationStatus(applicationId, status) {
    return api.post('/company/update-application-status', {
      application_id: applicationId,
      status: status
    })
  },

  getDashboard() {
    return api.get('/admin/dashboard')
  },

  getCompanies() {
    return api.get('/admin/companies')
  },

  approveCompany(companyId) {
    return api.post(`/admin/approve-company/${companyId}`)
  },

  rejectCompany(companyId) {
    return api.post(`/admin/reject-company/${companyId}`)
  }
}
