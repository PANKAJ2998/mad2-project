<template>
  <div class="student-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Student Dashboard</h2>
        <p class="text-muted mb-0" v-if="studentInfo.name">Welcome, {{ studentInfo.name }}</p>
      </div>
      <router-link to="/student/profile" class="btn btn-outline-primary">
        <i class="bi bi-person me-2"></i>My Profile
      </router-link>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <StatsCard
          title="Available Drives"
          :value="driveStore.drives.length"
          subtitle="Drives you're eligible for"
          icon="bi bi-briefcase"
          iconColor="primary"
        />
      </div>
      <div class="col-md-4">
        <StatsCard
          title="My Applications"
          :value="applicationStore.applications.length"
          subtitle="Total applications"
          icon="bi bi-file-earmark-text"
          iconColor="info"
        />
      </div>
      <div class="col-md-4">
        <StatsCard
          title="Selections"
          :value="selectedCount"
          subtitle="You've been selected"
          icon="bi bi-trophy"
          iconColor="success"
        />
      </div>
    </div>

    <div class="row g-4 mb-4">
      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Your Profile</h5>
            <div class="profile-info">
              <p><strong>Branch:</strong> {{ studentInfo.branch }}</p>
              <p><strong>CGPA:</strong> {{ studentInfo.cgpa }}</p>
              <p><strong>Graduation Year:</strong> {{ studentInfo.graduation_year }}</p>
            </div>
            <router-link to="/student/profile" class="btn btn-sm btn-outline-primary">
              Edit Profile
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">Quick Actions</h5>
            <div class="d-grid gap-2">
              <router-link to="/student/drives" class="btn btn-primary">
                <i class="bi bi-search me-2"></i>Browse Drives
              </router-link>
              <router-link to="/student/applications" class="btn btn-outline-primary">
                <i class="bi bi-list-ul me-2"></i>View My Applications
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div>
      <h4 class="mb-3">Recent Applications</h4>
      <Loader v-if="applicationStore.loading" message="Loading applications..." />

      <div v-else-if="applicationStore.applications.length === 0" class="text-center py-4 text-muted">
        <p>No applications yet. Start applying to drives!</p>
        <router-link to="/student/drives" class="btn btn-primary">
          Browse Drives
        </router-link>
      </div>

      <div v-else class="card">
        <div class="card-body">
          <ApplicationTable
            :applications="recentApplications"
            :columns="applicationColumns"
          />
          <div class="text-center mt-3" v-if="applicationStore.applications.length > 5">
            <router-link to="/student/applications" class="btn btn-link">
              View All Applications
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useDriveStore } from '@/stores/driveStore'
import { useApplicationStore } from '@/stores/applicationStore'
import StatsCard from '@/components/StatsCard.vue'
import ApplicationTable from '@/components/ApplicationTable.vue'
import Loader from '@/components/Loader.vue'

const authStore = useAuthStore()
const driveStore = useDriveStore()
const applicationStore = useApplicationStore()

const studentInfo = ref({})

const applicationColumns = [
  { key: 'drive.job_title', label: 'Job Title' },
  { key: 'drive.company_name', label: 'Company' },
  { key: 'application_date', label: 'Applied On' },
  { key: 'status', label: 'Status' }
]

onMounted(async () => {
  const userData = authStore.user
  if (userData && userData.student) {
    studentInfo.value = userData.student
  }

  await Promise.all([
    driveStore.fetchStudentDrives(),
    applicationStore.fetchMyApplications()
  ])
})

const selectedCount = computed(() => {
  return applicationStore.applications.filter(app => app.status === 'selected').length
})

const recentApplications = computed(() => {
  return applicationStore.applications.slice(0, 5)
})
</script>

<style scoped>
.profile-info p {
  margin-bottom: 0.5rem;
}
</style>
