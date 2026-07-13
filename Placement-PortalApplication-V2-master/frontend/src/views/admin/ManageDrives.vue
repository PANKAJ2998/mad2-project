<template>
  <div class="manage-drives">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Manage Placement Drives</h2>
      <router-link to="/admin/dashboard" class="btn btn-outline-primary">
        <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
      </router-link>
    </div>

    <Loader v-if="driveStore.loading" message="Loading drives..." />

    <div v-if="success" class="alert alert-success alert-dismissible fade show">
      {{ success }}
      <button type="button" class="btn-close" @click="success = null"></button>
    </div>

    <div v-if="error" class="alert alert-danger alert-dismissible fade show">
      {{ error }}
      <button type="button" class="btn-close" @click="error = null"></button>
    </div>

    <div v-if="driveStore.drives.length === 0 && !driveStore.loading" class="text-center py-5 text-muted">
      <i class="bi bi-briefcase display-1"></i>
      <p class="mt-3">No drives created yet</p>
    </div>

    <div class="row g-4" v-else>
      <div class="col-md-6 col-lg-4" v-for="drive in driveStore.drives" :key="drive.id">
        <DriveCard :drive="drive">
          <template #actions>
            <div class="d-grid gap-2">
              <button
                v-if="drive.status === 'pending'"
                class="btn btn-success btn-sm"
                @click="approveDrive(drive.id)"
                :disabled="processing"
              >
                <i class="bi bi-check-circle me-2"></i>Approve Drive
              </button>
              <span v-else class="badge bg-success w-100 py-2">
                Approved
              </span>
              <button
                class="btn btn-outline-secondary btn-sm"
                @click="editDrive(drive)"
              >
                <i class="bi bi-pencil me-2"></i>Edit Drive
              </button>
              <button
                class="btn btn-outline-danger btn-sm"
                @click="confirmDelete(drive.id)"
                :disabled="deleting"
              >
                <i class="bi bi-trash me-2"></i>Delete
              </button>
            </div>
          </template>
        </DriveCard>
      </div>
    </div>

    <!-- Edit Drive Modal -->
    <div v-if="showEditModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Drive</h5>
            <button type="button" class="btn-close" @click="showEditModal = false"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateDrive">
              <div class="mb-3">
                <label class="form-label">Job Title</label>
                <input type="text" class="form-control" v-model="editModalDrive.job_title" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Job Description</label>
                <textarea class="form-control" v-model="editModalDrive.job_description" rows="4"></textarea>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Minimum CGPA</label>
                  <input type="number" class="form-control" v-model.number="editModalDrive.eligibility_cgpa" step="0.01" min="0" max="10">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Graduation Year</label>
                  <input type="number" class="form-control" v-model.number="editModalDrive.eligibility_year" min="2024" max="2030">
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Eligible Branches</label>
                <input type="text" class="form-control" v-model="editModalDrive.eligibility_branch" placeholder="CSE,ECE,EEE">
              </div>
              <div class="mb-3">
                <label class="form-label">Deadline</label>
                <input type="datetime-local" class="form-control" v-model="editModalDrive.deadline" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Status</label>
                <select class="form-select" v-model="editModalDrive.status">
                  <option value="pending">Pending</option>
                  <option value="approved">Approved</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
              <div class="d-flex gap-2 justify-content-end">
                <button type="button" class="btn btn-secondary" @click="showEditModal = false">Cancel</button>
                <button type="submit" class="btn btn-primary" :disabled="updating">
                  <span v-if="updating">
                    <span class="spinner-border spinner-border-sm me-2"></span>Updating...
                  </span>
                  <span v-else>Update Drive</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useDriveStore } from '@/stores/driveStore'
import DriveCard from '@/components/DriveCard.vue'
import Loader from '@/components/Loader.vue'
import driveService from '@/services/driveService'

const router = useRouter()
const driveStore = useDriveStore()
const processing = ref(false)
const deleting = ref(false)
const updating = ref(false)
const success = ref(null)
const error = ref(null)
const editModalDrive = ref(null)
const showEditModal = ref(false)

onMounted(() => {
  driveStore.fetchAllDrives()
})

const approveDrive = async (driveId) => {
  processing.value = true
  try {
    await driveStore.approveDrive(driveId)
    success.value = 'Drive approved successfully'
    setTimeout(() => { success.value = null }, 3000)
  } catch (error) {
    console.error('Failed to approve drive:', error)
  } finally {
    processing.value = false
  }
}

const editDrive = (drive) => {
  editModalDrive.value = {
    ...drive,
    deadline: formatDateForInput(drive.deadline)
  }
  showEditModal.value = true
}

const formatDateForInput = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}-${month}-${day}T${hours}:${minutes}`
}

const updateDrive = async () => {
  updating.value = true
  error.value = null

  try {
    await driveService.updateDrive(editModalDrive.value.id, editModalDrive.value, true)
    await driveStore.fetchAllDrives()
    showEditModal.value = false
    success.value = 'Drive updated successfully!'
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update drive'
  } finally {
    updating.value = false
  }
}

const confirmDelete = async (driveId) => {
  if (!confirm('Are you sure you want to delete this drive? This action cannot be undone and will remove all associated applications.')) {
    return
  }

  deleting.value = true
  try {
    await driveService.deleteDrive(driveId, true)
    await driveStore.fetchAllDrives()
    success.value = 'Drive deleted successfully!'
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to delete drive'
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
</style>
