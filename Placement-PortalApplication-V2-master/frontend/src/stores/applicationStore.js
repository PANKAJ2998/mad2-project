import { defineStore } from 'pinia'
import applicationService from '@/services/applicationService'

export const useApplicationStore = defineStore('application', {
  state: () => ({
    applications: [],
    loading: false,
    error: null
  }),

  actions: {
    async applyToDrive(driveId) {
      this.loading = true
      this.error = null
      try {
        const response = await applicationService.applyToDrive(driveId)
        if (response.data.success) {
          return response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to apply'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchMyApplications() {
      this.loading = true
      this.error = null
      try {
        const response = await applicationService.getMyApplications()
        if (response.data.success) {
          this.applications = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch applications'
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateStatus(applicationId, status) {
      this.loading = true
      this.error = null
      try {
        const response = await applicationService.updateApplicationStatus(applicationId, status)
        if (response.data.success) {
          return response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update status'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
