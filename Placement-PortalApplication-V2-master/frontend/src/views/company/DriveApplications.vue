<template>
  <div class="drive-applications">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Drive Applications</h2>
      <router-link to="/company/dashboard" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-2"></i>Back
      </router-link>
    </div>

    <Loader v-if="loading" message="Loading applications..." />

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success alert-dismissible fade show">
      {{ success }}
      <button type="button" class="btn-close" @click="success = null"></button>
    </div>

    <div v-if="!loading && applications.length === 0" class="text-center py-5 text-muted">
      <i class="bi bi-file-earmark-text display-1"></i>
      <p class="mt-3">No applications received yet</p>
    </div>

    <div v-else-if="!loading" class="card">
      <div class="card-body">
        <ApplicationTable
          :applications="applications"
          :columns="columns"
          :show-actions="true"
          empty-message="No applications found for this drive"
        >
          <template #actions="{ application }">
            <div class="btn-group btn-group-sm">
              <button
                class="btn btn-outline-info"
                @click="updateStatus(application.id, 'shortlisted')"
                :disabled="processing"
                v-if="application.status !== 'shortlisted' && application.status !== 'selected'"
              >
                Shortlist
              </button>
              <button
                class="btn btn-outline-success"
                @click="updateStatus(application.id, 'selected')"
                :disabled="processing"
                v-if="application.status !== 'selected'"
              >
                Select
              </button>
              <button
                class="btn btn-outline-danger"
                @click="updateStatus(application.id, 'rejected')"
                :disabled="processing"
                v-if="application.status !== 'rejected'"
              >
                Reject
              </button>
            </div>
          </template>
        </ApplicationTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import driveService from '@/services/driveService'
import { useApplicationStore } from '@/stores/applicationStore'
import ApplicationTable from '@/components/ApplicationTable.vue'
import Loader from '@/components/Loader.vue'

const route = useRoute()
const applicationStore = useApplicationStore()

const applications = ref([])
const loading = ref(false)
const processing = ref(false)
const error = ref(null)
const success = ref(null)

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'student.name', label: 'Student Name' },
  { key: 'student.branch', label: 'Branch' },
  { key: 'student.cgpa', label: 'CGPA' },
  { key: 'student.graduation_year', label: 'Year' },
  { key: 'application_date', label: 'Applied On' },
  { key: 'status', label: 'Status' }
]

onMounted(() => {
  fetchApplications()
})

const fetchApplications = async () => {
  loading.value = true
  error.value = null
  try {
    const driveId = route.params.id
    const response = await driveService.getDriveApplications(driveId)
    if (response.data.success) {
      applications.value = response.data.data
    }
  } catch (err) {
    error.value = 'Failed to fetch applications'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (applicationId, status) => {
  processing.value = true
  error.value = null
  try {
    await applicationStore.updateStatus(applicationId, status)
    success.value = `Application ${status} successfully`
    await fetchApplications()
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = 'Failed to update status'
  } finally {
    processing.value = false
  }
}
</script>

<style scoped>
</style>
