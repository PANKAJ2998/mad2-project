<template>
  <div class="manage-companies">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Manage Companies</h2>
      <router-link to="/admin/dashboard" class="btn btn-outline-primary">
        <i class="bi bi-arrow-left me-2"></i>Back to Dashboard
      </router-link>
    </div>

    <Loader v-if="loading" message="Loading companies..." />

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success alert-dismissible fade show">
      {{ success }}
      <button type="button" class="btn-close" @click="success = null"></button>
    </div>

    <div class="row g-4" v-if="!loading">
      <div class="col-12" v-if="companies.length === 0">
        <div class="text-center py-5 text-muted">
          <i class="bi bi-building display-1"></i>
          <p class="mt-3">No companies registered yet</p>
        </div>
      </div>

      <div class="col-md-6 col-lg-4" v-for="company in companies" :key="company.id">
        <div class="card company-card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h5 class="card-title">{{ company.company_name }}</h5>
              <span :class="['badge', getStatusBadge(company.approval_status)]">
                {{ company.approval_status }}
              </span>
            </div>

            <div class="company-details">
              <p class="mb-2">
                <strong>Email:</strong> {{ company.user?.email || 'N/A' }}
              </p>
              <p class="mb-2" v-if="company.hr_contact">
                <strong>HR Contact:</strong> {{ company.hr_contact }}
              </p>
              <p class="mb-2" v-if="company.website">
                <strong>Website:</strong>
                <a :href="company.website" target="_blank" rel="noopener">
                  {{ company.website }}
                </a>
              </p>
              <p class="mb-0">
                <strong>Blacklisted:</strong>
                <span :class="company.is_blacklisted ? 'text-danger' : 'text-success'">
                  {{ company.is_blacklisted ? 'Yes' : 'No' }}
                </span>
              </p>
            </div>

            <div class="mt-3 d-flex gap-2" v-if="company.approval_status === 'pending'">
              <button
                class="btn btn-success btn-sm flex-fill"
                @click="approveCompany(company.id)"
                :disabled="processing"
              >
                <i class="bi bi-check-circle me-1"></i>Approve
              </button>
              <button
                class="btn btn-danger btn-sm flex-fill"
                @click="rejectCompany(company.id)"
                :disabled="processing"
              >
                <i class="bi bi-x-circle me-1"></i>Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import applicationService from '@/services/applicationService'
import Loader from '@/components/Loader.vue'

const companies = ref([])
const loading = ref(false)
const processing = ref(false)
const error = ref(null)
const success = ref(null)

onMounted(() => {
  fetchCompanies()
})

const fetchCompanies = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await applicationService.getCompanies()
    if (response.data.success) {
      companies.value = response.data.data
    }
  } catch (err) {
    error.value = 'Failed to fetch companies'
  } finally {
    loading.value = false
  }
}

const approveCompany = async (companyId) => {
  processing.value = true
  error.value = null
  try {
    await applicationService.approveCompany(companyId)
    success.value = 'Company approved successfully'
    await fetchCompanies()
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = 'Failed to approve company'
  } finally {
    processing.value = false
  }
}

const rejectCompany = async (companyId) => {
  processing.value = true
  error.value = null
  try {
    await applicationService.rejectCompany(companyId)
    success.value = 'Company rejected'
    await fetchCompanies()
    setTimeout(() => { success.value = null }, 3000)
  } catch (err) {
    error.value = 'Failed to reject company'
  } finally {
    processing.value = false
  }
}

const getStatusBadge = (status) => {
  switch (status) {
    case 'approved':
      return 'bg-success'
    case 'pending':
      return 'bg-warning text-dark'
    case 'rejected':
      return 'bg-danger'
    default:
      return 'bg-secondary'
  }
}
</script>

<style scoped>
.company-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.company-card:hover {
  transform: translateY(-3px);
}

.company-details {
  font-size: 0.9rem;
}

.company-details a {
  color: #007bff;
  text-decoration: none;
}

.company-details a:hover {
  text-decoration: underline;
}
</style>
