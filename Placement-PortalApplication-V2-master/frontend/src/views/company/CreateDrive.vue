<template>
  <div class="create-drive">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>{{ isEditMode ? 'Edit' : 'Create' }} Placement Drive</h2>
      <router-link to="/company/dashboard" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-2"></i>Back
      </router-link>
    </div>

    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow">
          <div class="card-body p-4">
            <div v-if="error" class="alert alert-danger alert-dismissible fade show">
              {{ error }}
              <button type="button" class="btn-close" @click="error = null"></button>
            </div>

            <div v-if="success" class="alert alert-success">
              Drive {{ isEditMode ? 'updated' : 'created' }} successfully!
              {{ !isEditMode ? 'It will be visible after admin approval.' : '' }}
            </div>

            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="job_title" class="form-label">Job Title *</label>
                <input
                  type="text"
                  class="form-control"
                  id="job_title"
                  v-model="form.job_title"
                  required
                />
              </div>

              <div class="mb-3">
                <label for="job_description" class="form-label">Job Description</label>
                <textarea
                  class="form-control"
                  id="job_description"
                  rows="4"
                  v-model="form.job_description"
                ></textarea>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="eligibility_cgpa" class="form-label">Minimum CGPA</label>
                  <input
                    type="number"
                    class="form-control"
                    id="eligibility_cgpa"
                    v-model.number="form.eligibility_cgpa"
                    step="0.01"
                    min="0"
                    max="10"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label for="eligibility_year" class="form-label">Graduation Year</label>
                  <input
                    type="number"
                    class="form-control"
                    id="eligibility_year"
                    v-model.number="form.eligibility_year"
                    min="2024"
                    max="2030"
                  />
                </div>
              </div>

              <div class="mb-3">
                <label for="eligibility_branch" class="form-label">Eligible Branches</label>
                <input
                  type="text"
                  class="form-control"
                  id="eligibility_branch"
                  v-model="form.eligibility_branch"
                  placeholder="e.g., CSE,ECE,EEE (comma separated)"
                />
                <div class="form-text">Leave blank for all branches</div>
              </div>

              <div class="mb-3">
                <label for="deadline" class="form-label">Application Deadline *</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  id="deadline"
                  v-model="form.deadline"
                  required
                />
              </div>

              <div class="alert alert-info" v-if="!isEditMode">
                <small>
                  <i class="bi bi-info-circle me-2"></i>
                  Your drive will be reviewed by admin before students can view it.
                </small>
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="driveStore.loading">
                <span v-if="driveStore.loading">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  {{ isEditMode ? 'Updating' : 'Creating' }} Drive...
                </span>
                <span v-else>{{ isEditMode ? 'Update' : 'Create' }} Drive</span>
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useDriveStore } from '@/stores/driveStore'
import driveService from '@/services/driveService'

const router = useRouter()
const route = useRoute()
const driveStore = useDriveStore()

const isEditMode = ref(false)
const editDriveId = ref(null)

const form = ref({
  job_title: '',
  job_description: '',
  eligibility_cgpa: 0,
  eligibility_branch: '',
  eligibility_year: null,
  deadline: ''
})

const error = ref(null)
const success = ref(false)

onMounted(async () => {
  if (route.query.edit) {
    isEditMode.value = true
    editDriveId.value = parseInt(route.query.edit)
    await loadDriveData()
  }
})

const loadDriveData = async () => {
  try {
    await driveStore.fetchCompanyDrives()
    const drive = driveStore.drives.find(d => d.id === editDriveId.value)

    if (drive) {
      form.value = {
        job_title: drive.job_title,
        job_description: drive.job_description || '',
        eligibility_cgpa: drive.eligibility_cgpa || 0,
        eligibility_branch: drive.eligibility_branch || '',
        eligibility_year: drive.eligibility_year || null,
        deadline: formatDateForInput(drive.deadline)
      }
    } else {
      error.value = 'Drive not found'
    }
  } catch (err) {
    error.value = 'Failed to load drive data'
  }
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

const handleSubmit = async () => {
  error.value = null
  success.value = false

  try {
    if (isEditMode.value) {
      await driveService.updateDrive(editDriveId.value, form.value, false)
      success.value = true
      setTimeout(() => {
        router.push('/company/dashboard')
      }, 1500)
    } else {
      await driveStore.createDrive(form.value)
      success.value = true
      setTimeout(() => {
        router.push('/company/dashboard')
      }, 2000)
    }
  } catch (err) {
    error.value = err.response?.data?.message || `Failed to ${isEditMode.value ? 'update' : 'create'} drive`
  }
}
</script>

<style scoped>
</style>
