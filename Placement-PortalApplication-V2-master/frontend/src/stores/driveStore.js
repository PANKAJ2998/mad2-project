import { defineStore } from 'pinia'
import driveService from '@/services/driveService'

export const useDriveStore = defineStore('drive', {
  state: () => ({
    drives: [],
    currentDrive: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchStudentDrives() {
      this.loading = true
      this.error = null
      try {
        const response = await driveService.getStudentDrives()
        if (response.data.success) {
          this.drives = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch drives'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchCompanyDrives() {
      this.loading = true
      this.error = null
      try {
        const response = await driveService.getCompanyDrives()
        if (response.data.success) {
          this.drives = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch drives'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchAllDrives() {
      this.loading = true
      this.error = null
      try {
        const response = await driveService.getAllDrives()
        if (response.data.success) {
          this.drives = response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to fetch drives'
        throw error
      } finally {
        this.loading = false
      }
    },

    async createDrive(data) {
      this.loading = true
      this.error = null
      try {
        const response = await driveService.createDrive(data)
        if (response.data.success) {
          return response.data.data
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to create drive'
        throw error
      } finally {
        this.loading = false
      }
    },

    async approveDrive(driveId) {
      this.loading = true
      this.error = null
      try {
        const response = await driveService.approveDrive(driveId)
        if (response.data.success) {
          await this.fetchAllDrives()
          return true
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to approve drive'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
