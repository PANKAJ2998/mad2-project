<template>
  <div class="company-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>Company Dashboard</h2>
        <p class="text-muted mb-0" v-if="authStore.user">{{ companyInfo.company_name }}</p>
      </div>
      <router-link to="/company/create-drive" class="btn btn-primary">
        <i class="bi bi-plus-circle me-2"></i>Create Drive
      </router-link>
    </div>

    <div v-if="approvalWarning" class="alert alert-warning">
      <i class="bi bi-exclamation-triangle me-2"></i>
      Your company account is pending admin approval. You'll be able to create drives once approved.
    </div>

    <div class="row g-4 mb-4">
      <div class="col-md-4">
        <StatsCard
          title="Total Drives"
          :value="driveStore.drives.length"
          subtitle="Drives created"
          icon="bi bi-briefcase"
          iconColor="primary"
        />
      </div>
      <div class="col-md-4">
        <StatsCard
          title="Pending Approval"
          :value="pendingDrives"
          subtitle="Awaiting admin approval"
          icon="bi bi-clock-history"
          iconColor="warning"
        />
      </div>
      <div class="col-md-4">
        <StatsCard
          title="Active Drives"
          :value="activeDrives"
          subtitle="Currently accepting applications"
          icon="bi bi-check-circle"
          iconColor="success"
        />
      </div>
    </div>

    <Loader v-if="driveStore.loading" message="Loading your drives..." />

    <div v-else>
      <h4 class="mb-3">My Placement Drives</h4>

      <div v-if="driveStore.drives.length === 0" class="text-center py-5 text-muted">
        <i class="bi bi-briefcase display-1"></i>
        <p class="mt-3">No drives created yet</p>
        <router-link to="/company/create-drive" class="btn btn-primary">
          Create Your First Drive
        </router-link>
      </div>

      <div class="row g-4" v-else>
        <div class="col-md-6 col-lg-4" v-for="drive in driveStore.drives" :key="drive.id">
          <DriveCard :drive="drive">
            <template #actions>
              <div class="d-grid gap-2">
                <router-link
                  :to="`/company/drive-applications/${drive.id}`"
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="bi bi-list-ul me-2"></i>View Applications
                </router-link>
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
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useDriveStore } from '@/stores/driveStore'
import StatsCard from '@/components/StatsCard.vue'
import DriveCard from '@/components/DriveCard.vue'
import Loader from '@/components/Loader.vue'
import driveService from '@/services/driveService'

const router = useRouter()
const authStore = useAuthStore()
const driveStore = useDriveStore()

const companyInfo = ref({})
const approvalWarning = ref(false)
const deleting = ref(false)

onMounted(async () => {
  const userData = authStore.user
  if (userData && userData.company) {
    companyInfo.value = userData.company
    approvalWarning.value = userData.company.approval_status !== 'approved'
  }

  await driveStore.fetchCompanyDrives()
})

const pendingDrives = computed(() => {
  return driveStore.drives.filter(d => d.status === 'pending').length
})

const activeDrives = computed(() => {
  return driveStore.drives.filter(d => d.status === 'approved').length
})

const editDrive = (drive) => {
  router.push({
    name: 'CreateDrive',
    query: { edit: drive.id }
  })
}

const confirmDelete = async (driveId) => {
  if (!confirm('Are you sure you want to delete this drive? This action cannot be undone.')) {
    return
  }

  deleting.value = true
  try {
    await driveService.deleteDrive(driveId, false)
    await driveStore.fetchCompanyDrives()
    alert('Drive deleted successfully!')
  } catch (error) {
    alert(error.response?.data?.message || 'Failed to delete drive')
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
</style>
