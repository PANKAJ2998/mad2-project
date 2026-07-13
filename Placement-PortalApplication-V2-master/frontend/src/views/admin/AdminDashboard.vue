<template>
  <div class="admin-dashboard">
    <h2 class="mb-4">Admin Dashboard - Analytics</h2>

    <Loader v-if="loading" message="Loading analytics..." />

    <div v-else-if="dashboardData">
      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-4">
          <StatsCard
            title="Total Companies"
            :value="stats.companies.total"
            :subtitle="`${stats.companies.pending} pending approval`"
            icon="bi bi-building"
            iconColor="primary"
          />
        </div>
        <div class="col-md-4">
          <StatsCard
            title="Total Drives"
            :value="stats.drives.total"
            :subtitle="`${stats.drives.pending} pending approval`"
            icon="bi bi-briefcase"
            iconColor="success"
          />
        </div>
        <div class="col-md-4">
          <StatsCard
            title="Total Applications"
            :value="stats.applications.total"
            :subtitle="`${stats.applications.selected} selected`"
            icon="bi bi-file-earmark-text"
            iconColor="info"
          />
        </div>
      </div>

      <!-- Analytics Charts -->
      <div class="row g-4 mb-4">
        <div class="col-lg-6">
          <div class="card chart-card">
            <div class="card-body">
              <h5 class="card-title mb-3">
                <i class="bi bi-building me-2"></i>Companies Analytics
              </h5>
              <div class="chart-container">
                <canvas id="companiesChart"></canvas>
              </div>
              <div class="chart-legend mt-3">
                <span class="badge bg-success me-2">Approved: {{ stats.companies.approved }}</span>
                <span class="badge bg-warning text-dark me-2">Pending: {{ stats.companies.pending }}</span>
                <span class="badge bg-secondary">Total: {{ stats.companies.total }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="card chart-card">
            <div class="card-body">
              <h5 class="card-title mb-3">
                <i class="bi bi-briefcase me-2"></i>Placement Drives Analytics
              </h5>
              <div class="chart-container">
                <canvas id="drivesChart"></canvas>
              </div>
              <div class="chart-legend mt-3">
                <span class="badge bg-primary me-2">Approved: {{ stats.drives.approved }}</span>
                <span class="badge bg-warning text-dark me-2">Pending: {{ stats.drives.pending }}</span>
                <span class="badge bg-secondary">Total: {{ stats.drives.total }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Applications Chart -->
      <div class="row g-4 mb-4">
        <div class="col-12">
          <div class="card chart-card">
            <div class="card-body">
              <h5 class="card-title mb-3">
                <i class="bi bi-graph-up me-2"></i>Applications Analytics
              </h5>
              <div class="chart-container">
                <canvas id="applicationsChart"></canvas>
              </div>
              <div class="chart-legend mt-3">
                <span class="badge bg-info me-2">Total: {{ stats.applications.total }}</span>
                <span class="badge bg-success me-2">Selected: {{ stats.applications.selected }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="text-center mt-4">
        <router-link to="/admin/companies" class="btn btn-primary me-2">
          <i class="bi bi-building me-1"></i> Manage Companies
        </router-link>
        <router-link to="/admin/drives" class="btn btn-success">
          <i class="bi bi-briefcase me-1"></i> Manage Drives
        </router-link>
      </div>
    </div>

    <!-- Error State -->
    <div v-else class="alert alert-warning">
      <i class="bi bi-exclamation-triangle me-2"></i>
      Unable to load dashboard data. Please refresh the page.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { Chart } from 'chart.js/auto'
import applicationService from '@/services/applicationService'
import StatsCard from '@/components/StatsCard.vue'
import Loader from '@/components/Loader.vue'

const loading = ref(false)
const dashboardData = ref(null)

let companiesChartInstance = null
let drivesChartInstance = null
let applicationsChartInstance = null

const stats = computed(() => {
  if (!dashboardData.value) {
    return {
      companies: { total: 0, pending: 0, approved: 0 },
      drives: { total: 0, pending: 0, approved: 0 },
      applications: { total: 0, selected: 0 }
    }
  }
  return dashboardData.value
})

onMounted(async () => {
  console.log('AdminDashboard mounted')
  await fetchDashboardData()
})

onBeforeUnmount(() => {
  destroyCharts()
})

const destroyCharts = () => {
  if (companiesChartInstance) {
    companiesChartInstance.destroy()
    companiesChartInstance = null
  }
  if (drivesChartInstance) {
    drivesChartInstance.destroy()
    drivesChartInstance = null
  }
  if (applicationsChartInstance) {
    applicationsChartInstance.destroy()
    applicationsChartInstance = null
  }
}

const fetchDashboardData = async () => {
  loading.value = true
  try {
    console.log('Fetching dashboard data...')
    const response = await applicationService.getDashboard()
    console.log('Dashboard response:', response.data)
    
    if (response.data.success) {
      dashboardData.value = response.data.data
      console.log('Dashboard data set:', dashboardData.value)
      
      // Wait for next tick and render charts
      setTimeout(() => {
        renderCharts()
      }, 100)
    } else {
      console.error('Failed to fetch dashboard data:', response.data.message)
      dashboardData.value = {
        companies: { total: 0, pending: 0, approved: 0 },
        drives: { total: 0, pending: 0, approved: 0 },
        applications: { total: 0, selected: 0 }
      }
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
    dashboardData.value = {
      companies: { total: 0, pending: 0, approved: 0 },
      drives: { total: 0, pending: 0, approved: 0 },
      applications: { total: 0, selected: 0 }
    }
    setTimeout(() => {
      renderCharts()
    }, 100)
  } finally {
    loading.value = false
  }
}

const renderCharts = () => {
  console.log('Rendering charts...')
  destroyCharts()

  try {
    const data = dashboardData.value
    if (!data) {
      console.error('No dashboard data available')
      return
    }

    // Companies Chart
    const companiesCanvas = document.getElementById('companiesChart')
    if (companiesCanvas) {
      console.log('Creating companies chart with data:', data.companies)
      companiesChartInstance = new Chart(companiesCanvas, {
        type: 'doughnut',
        data: {
          labels: ['Approved', 'Pending', 'Rejected'],
          datasets: [{
            label: 'Companies',
            data: [
              data.companies.approved || 0,
              data.companies.pending || 0,
              (data.companies.total - data.companies.approved - data.companies.pending) || 0
            ],
            backgroundColor: [
              'rgba(40, 167, 69, 0.8)',
              'rgba(255, 193, 7, 0.8)',
              'rgba(220, 53, 69, 0.8)'
            ],
            borderColor: [
              'rgba(40, 167, 69, 1)',
              'rgba(255, 193, 7, 1)',
              'rgba(220, 53, 69, 1)'
            ],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 15,
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || ''
                  const value = context.parsed || 0
                  const total = context.dataset.data.reduce((a, b) => a + b, 0)
                  const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
                  return `${label}: ${value} (${percentage}%)`
                }
              }
            }
          }
        }
      })
      console.log('Companies chart created successfully')
    } else {
      console.error('Companies canvas not found')
    }

    // Drives Chart
    const drivesCanvas = document.getElementById('drivesChart')
    if (drivesCanvas) {
      console.log('Creating drives chart with data:', data.drives)
      drivesChartInstance = new Chart(drivesCanvas, {
        type: 'pie',
        data: {
          labels: ['Approved', 'Pending', 'Rejected'],
          datasets: [{
            label: 'Drives',
            data: [
              data.drives.approved || 0,
              data.drives.pending || 0,
              (data.drives.total - data.drives.approved - data.drives.pending) || 0
            ],
            backgroundColor: [
              'rgba(0, 123, 255, 0.8)',
              'rgba(255, 193, 7, 0.8)',
              'rgba(220, 53, 69, 0.8)'
            ],
            borderColor: [
              'rgba(0, 123, 255, 1)',
              'rgba(255, 193, 7, 1)',
              'rgba(220, 53, 69, 1)'
            ],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                padding: 15,
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || ''
                  const value = context.parsed || 0
                  const total = context.dataset.data.reduce((a, b) => a + b, 0)
                  const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0
                  return `${label}: ${value} (${percentage}%)`
                }
              }
            }
          }
        }
      })
      console.log('Drives chart created successfully')
    } else {
      console.error('Drives canvas not found')
    }

    // Applications Chart
    const applicationsCanvas = document.getElementById('applicationsChart')
    if (applicationsCanvas) {
      console.log('Creating applications chart with data:', data.applications)
      applicationsChartInstance = new Chart(applicationsCanvas, {
        type: 'bar',
        data: {
          labels: ['Total Applications', 'Selected', 'Pending', 'Rejected'],
          datasets: [{
            label: 'Application Status',
            data: [
              data.applications.total || 0,
              data.applications.selected || 0,
              Math.max(0, (data.applications.total - data.applications.selected) / 2) || 0,
              Math.max(0, (data.applications.total - data.applications.selected) / 2) || 0
            ],
            backgroundColor: [
              'rgba(23, 162, 184, 0.8)',
              'rgba(40, 167, 69, 0.8)',
              'rgba(255, 193, 7, 0.8)',
              'rgba(220, 53, 69, 0.8)'
            ],
            borderColor: [
              'rgba(23, 162, 184, 1)',
              'rgba(40, 167, 69, 1)',
              'rgba(255, 193, 7, 1)',
              'rgba(220, 53, 69, 1)'
            ],
            borderWidth: 2,
            borderRadius: 5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                precision: 0,
                font: {
                  size: 11
                }
              }
            },
            x: {
              ticks: {
                font: {
                  size: 11
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.parsed.y}`
                }
              }
            }
          }
        }
      })
      console.log('Applications chart created successfully')
    } else {
      console.error('Applications canvas not found')
    }
  } catch (error) {
    console.error('Error rendering charts:', error)
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 1rem 0;
}

.card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.chart-card {
  height: 100%;
}

.card-body {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.chart-container {
  position: relative;
  height: 280px;
  width: 100%;
  margin: 0 auto;
}

canvas {
  max-width: 100%;
  max-height: 100%;
}

.chart-legend {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.chart-legend .badge {
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
  font-weight: 500;
}

.alert {
  border-radius: 8px;
  padding: 1.25rem;
}

.btn {
  padding: 0.625rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

@media (max-width: 768px) {
  .chart-container {
    height: 240px;
  }
  
  .card-body {
    padding: 1rem;
  }
}
</style>
