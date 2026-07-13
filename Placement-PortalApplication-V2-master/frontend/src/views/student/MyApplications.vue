<template>
  <div class="my-applications">
    <h2 class="mb-4">My Applications</h2>

    <Loader v-if="applicationStore.loading" message="Loading your applications..." />

    <div v-else-if="applicationStore.applications.length === 0" class="text-center py-5 text-muted">
      <i class="bi bi-file-earmark-text display-1"></i>
      <p class="mt-3">You haven't applied to any drives yet</p>
      <router-link to="/student/drives" class="btn btn-primary">
        <i class="bi bi-search me-2"></i>Browse Drives
      </router-link>
    </div>

    <div v-else>
      <div class="mb-4">
        <div class="btn-group" role="group">
          <button
            type="button"
            :class="['btn', filterStatus === 'all' ? 'btn-primary' : 'btn-outline-primary']"
            @click="filterStatus = 'all'"
          >
            All ({{ applicationStore.applications.length }})
          </button>
          <button
            type="button"
            :class="['btn', filterStatus === 'applied' ? 'btn-primary' : 'btn-outline-primary']"
            @click="filterStatus = 'applied'"
          >
            Applied ({{ countByStatus('applied') }})
          </button>
          <button
            type="button"
            :class="['btn', filterStatus === 'shortlisted' ? 'btn-primary' : 'btn-outline-primary']"
            @click="filterStatus = 'shortlisted'"
          >
            Shortlisted ({{ countByStatus('shortlisted') }})
          </button>
          <button
            type="button"
            :class="['btn', filterStatus === 'selected' ? 'btn-primary' : 'btn-outline-primary']"
            @click="filterStatus = 'selected'"
          >
            Selected ({{ countByStatus('selected') }})
          </button>
          <button
            type="button"
            :class="['btn', filterStatus === 'rejected' ? 'btn-primary' : 'btn-outline-primary']"
            @click="filterStatus = 'rejected'"
          >
            Rejected ({{ countByStatus('rejected') }})
          </button>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <ApplicationTable
            :applications="filteredApplications"
            :columns="columns"
            :empty-message="`No ${filterStatus} applications`"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '@/stores/applicationStore'
import ApplicationTable from '@/components/ApplicationTable.vue'
import Loader from '@/components/Loader.vue'

const applicationStore = useApplicationStore()
const filterStatus = ref('all')

const columns = [
  { key: 'id', label: 'ID' },
  { key: 'drive.job_title', label: 'Job Title' },
  { key: 'drive.company_name', label: 'Company' },
  { key: 'application_date', label: 'Applied On' },
  { key: 'drive.deadline', label: 'Deadline' },
  { key: 'status', label: 'Status' }
]

onMounted(() => {
  applicationStore.fetchMyApplications()
})

const filteredApplications = computed(() => {
  if (filterStatus.value === 'all') {
    return applicationStore.applications
  }
  return applicationStore.applications.filter(app => app.status === filterStatus.value)
})

const countByStatus = (status) => {
  return applicationStore.applications.filter(app => app.status === status).length
}
</script>

<style scoped>
</style>
