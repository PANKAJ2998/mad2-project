<template>
  <div class="card drive-card h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title">{{ drive.job_title }}</h5>
        <span
          :class="['badge', statusBadgeClass]"
        >
          {{ drive.status }}
        </span>
      </div>

      <h6 class="text-muted mb-3">{{ drive.company_name }}</h6>

      <p class="card-text">{{ truncatedDescription }}</p>

      <div class="drive-details">
        <div class="detail-item" v-if="drive.eligibility_cgpa">
          <strong>Min CGPA:</strong> {{ drive.eligibility_cgpa }}
        </div>
        <div class="detail-item" v-if="drive.eligibility_branch">
          <strong>Branches:</strong> {{ drive.eligibility_branch }}
        </div>
        <div class="detail-item" v-if="drive.eligibility_year">
          <strong>Year:</strong> {{ drive.eligibility_year }}
        </div>
        <div class="detail-item">
          <strong>Deadline:</strong> {{ formattedDeadline }}
        </div>
      </div>

      <div class="mt-3" v-if="showActions">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  drive: {
    type: Object,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
})

const truncatedDescription = computed(() => {
  if (!props.drive.job_description) return 'No description available'
  return props.drive.job_description.length > 150
    ? props.drive.job_description.substring(0, 150) + '...'
    : props.drive.job_description
})

const formattedDeadline = computed(() => {
  if (!props.drive.deadline) return 'N/A'
  const date = new Date(props.drive.deadline)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
})

const statusBadgeClass = computed(() => {
  const status = props.drive.status?.toLowerCase()
  switch (status) {
    case 'approved':
      return 'bg-success'
    case 'pending':
      return 'bg-warning text-dark'
    case 'closed':
      return 'bg-secondary'
    default:
      return 'bg-info'
  }
})
</script>

<style scoped>
.drive-card {
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid #e0e0e0;
}

.drive-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  color: #333;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.drive-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e0e0e0;
}

.detail-item {
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.detail-item strong {
  color: #666;
  margin-right: 0.5rem;
}
</style>
