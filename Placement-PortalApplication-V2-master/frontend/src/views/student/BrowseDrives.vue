<template>
  <div class="browse-drives">
    <h2 class="mb-4">Browse Placement Drives</h2>

    <div v-if="profileIncomplete" class="alert alert-warning alert-dismissible fade show">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      Your profile is incomplete. Please update your profile to see drives you're eligible for.
      <router-link to="/student/profile" class="alert-link ms-2">Update Profile</router-link>
      <button type="button" class="btn-close" @click="profileIncomplete = false"></button>
    </div>

    <Loader v-if="driveStore.loading" message="Loading available drives..." />

    <div v-if="success" class="alert alert-success alert-dismissible fade show">
      {{ success }}
      <button type="button" class="btn-close" @click="success = null"></button>
    </div>

    <div v-if="error" class="alert alert-danger alert-dismissible fade show">
      {{ error }}
      <button type="button" class="btn-close" @click="error = null"></button>
    </div>

    <div v-if="!driveStore.loading && driveStore.drives.length === 0" class="text-center py-5">
      <div class="empty-state">
        <i class="bi bi-briefcase display-1 text-muted mb-3"></i>
        <h4 class="text-muted">No Drives Available</h4>
        <p class="text-muted">There are no placement drives available at the moment.</p>
        <div class="d-flex gap-2 justify-content-center flex-wrap">
          <p class="text-muted small">This could be because:</p>
        </div>
        <ul class="list-unstyled text-muted small">
          <li>• No drives have been created yet</li>
          <li>• Drives are pending admin approval</li>
          <li>• You don't meet the eligibility criteria for current drives</li>
          <li>• All drive deadlines have passed</li>
        </ul>
        <router-link to="/student/dashboard" class="btn btn-primary mt-3">
          <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
        </router-link>
      </div>
    </div>

    <div class="row g-4" v-else-if="!driveStore.loading">
      <div class="col-md-6 col-lg-4" v-for="drive in driveStore.drives" :key="drive.id">
        <DriveCard :drive="drive">
          <template #actions>
            <button
              class="btn btn-primary w-100"
              @click="applyToDrive(drive.id)"
              :disabled="processing || hasApplied(drive.id)"
            >
              <span v-if="processing">
                <span class="spinner-border spinner-border-sm me-2"></span>
                Applying...
              </span>
              <span v-else-if="hasApplied(drive.id)">
                <i class="bi bi-check-circle me-2"></i>Applied
              </span>
              <span v-else>
                <i class="bi bi-send me-2"></i>Apply Now
              </span>
            </button>
          </template>
        </DriveCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDriveStore } from '@/stores/driveStore'
import { useApplicationStore } from '@/stores/applicationStore'
import { useAuthStore } from '@/stores/authStore'
import DriveCard from '@/components/DriveCard.vue'
import Loader from '@/components/Loader.vue'

const authStore = useAuthStore()
const driveStore = useDriveStore()
const applicationStore = useApplicationStore()

const processing = ref(false)
const error = ref(null)
const success = ref(null)
const profileIncomplete = ref(false)

const checkProfileComplete = () => {
  const student = authStore.user?.student
  if (!student || !student.branch || !student.cgpa || !student.graduation_year) {
    profileIncomplete.value = true
    return false
  }
  return true
}

onMounted(async () => {
  checkProfileComplete()

  try {
    await Promise.all([
      driveStore.fetchStudentDrives(),
      applicationStore.fetchMyApplications()
    ])
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to load drives'
  }
})

const hasApplied = (driveId) => {
  return applicationStore.applications.some(app => app.drive_id === driveId)
}

const applyToDrive = async (driveId) => {
  if (hasApplied(driveId)) return

  processing.value = true
  error.value = null
  success.value = null

  try {
    await applicationStore.applyToDrive(driveId)
    await applicationStore.fetchMyApplications()
    success.value = 'Application submitted successfully!'
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to apply. Please try again.'
  } finally {
    processing.value = false
  }
}
</script>

<style scoped>
.empty-state {
  max-width: 500px;
  margin: 0 auto;
}
</style>
