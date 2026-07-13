<template>
  <div class="student-profile">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>My Profile</h2>
      <router-link to="/student/dashboard" class="btn btn-outline-secondary">
        <i class="bi bi-arrow-left me-2"></i>Back
      </router-link>
    </div>

    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow">
          <div class="card-body p-4">
            <div v-if="loading" class="text-center py-5">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="text-muted mt-2">Loading profile...</p>
            </div>

            <div v-else>
              <div v-if="success" class="alert alert-success alert-dismissible fade show">
                {{ success }}
                <button type="button" class="btn-close" @click="success = null"></button>
              </div>

              <div v-if="error" class="alert alert-danger alert-dismissible fade show">
                {{ error }}
                <button type="button" class="btn-close" @click="error = null"></button>
              </div>

              <div class="mb-4">
                <h5 class="text-muted">Personal Information</h5>
                <hr />
              </div>

              <form @submit.prevent="handleUpdate">
              <div class="mb-3">
                <label for="name" class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control"
                  id="name"
                  v-model="form.name"
                  readonly
                />
                <div class="form-text">Contact admin to change your name</div>
              </div>

              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  :value="authStore.user?.email"
                  readonly
                />
              </div>

              <div class="mb-3">
                <label for="branch" class="form-label">Branch</label>
                <select class="form-select" id="branch" v-model="form.branch">
                  <option value="CSE">Computer Science</option>
                  <option value="ECE">Electronics</option>
                  <option value="EEE">Electrical</option>
                  <option value="MECH">Mechanical</option>
                  <option value="CIVIL">Civil</option>
                </select>
              </div>

              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="cgpa" class="form-label">CGPA</label>
                  <input
                    type="number"
                    class="form-control"
                    id="cgpa"
                    v-model.number="form.cgpa"
                    step="0.01"
                    min="0"
                    max="10"
                  />
                </div>

                <div class="col-md-6 mb-3">
                  <label for="graduation_year" class="form-label">Graduation Year</label>
                  <input
                    type="number"
                    class="form-control"
                    id="graduation_year"
                    v-model.number="form.graduation_year"
                    min="2024"
                    max="2030"
                  />
                </div>
              </div>

              <div class="mb-3">
                <label for="resume" class="form-label">Resume</label>
                <input
                  type="file"
                  class="form-control"
                  id="resume"
                  accept=".pdf,.doc,.docx"
                  @change="handleFileUpload"
                />
                <div class="form-text">
                  <small>Upload your resume (PDF, DOC, DOCX - Max 5MB)</small>
                </div>
                <div v-if="form.resume_path" class="mt-2">
                  <span class="badge bg-success">
                    <i class="bi bi-file-earmark-check me-1"></i>
                    Resume uploaded
                  </span>
                </div>
              </div>

              <div class="alert alert-info">
                <small>
                  <i class="bi bi-info-circle me-2"></i>
                  Keep your profile updated to ensure accurate eligibility for placement drives.
                </small>
              </div>

              <button type="submit" class="btn btn-primary w-100" :disabled="updating">
                <span v-if="updating">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Updating...
                </span>
                <span v-else>
                  <i class="bi bi-save me-2"></i>Update Profile
                </span>
              </button>
            </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import studentService from '@/services/studentService'

const authStore = useAuthStore()

const form = ref({
  name: '',
  branch: '',
  cgpa: 0,
  graduation_year: 2024,
  resume_path: ''
})

const updating = ref(false)
const loading = ref(false)
const success = ref(null)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    // Fetch the latest profile data from backend
    const response = await studentService.getProfile()
    if (response.data.success && response.data.data) {
      const student = response.data.data
      form.value = {
        name: student.name || '',
        branch: student.branch || '',
        cgpa: student.cgpa || 0,
        graduation_year: student.graduation_year || 2024,
        resume_path: student.resume_path || ''
      }
    }
  } catch (err) {
    // Fallback to auth store if API fails
    const student = authStore.user?.student
    if (student) {
      form.value = {
        name: student.name || '',
        branch: student.branch || '',
        cgpa: student.cgpa || 0,
        graduation_year: student.graduation_year || 2024,
        resume_path: student.resume_path || ''
      }
    } else {
      error.value = 'Failed to load profile data. Please try refreshing the page.'
    }
  } finally {
    loading.value = false
  }
})

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      error.value = 'File size must be less than 5MB'
      event.target.value = ''
      return
    }
    form.value.resume_path = file.name
  }
}

const handleUpdate = async () => {
  updating.value = true
  error.value = null
  success.value = null

  try {
    const response = await studentService.updateProfile(form.value)
    if (response.data.success) {
      success.value = 'Profile updated successfully!'

      // Update the user data in auth store
      if (authStore.user && authStore.user.student) {
        authStore.user.student = response.data.data
      }

      // Refresh the form with updated data
      const student = response.data.data
      form.value = {
        name: student.name || '',
        branch: student.branch || '',
        cgpa: student.cgpa || 0,
        graduation_year: student.graduation_year || 2024,
        resume_path: student.resume_path || ''
      }

      // Clear success message after 3 seconds
      setTimeout(() => {
        success.value = null
      }, 3000)
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to update profile'
  } finally {
    updating.value = false
  }
}
</script>

<style scoped>
</style>
