<template>
  <div class="table-responsive">
    <table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
          <th v-if="showActions">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="applications.length === 0">
          <td :colspan="columns.length + (showActions ? 1 : 0)" class="text-center text-muted py-4">
            {{ emptyMessage }}
          </td>
        </tr>
        <tr v-for="application in applications" :key="application.id">
          <td v-for="column in columns" :key="column.key">
            <template v-if="column.key === 'status'">
              <span :class="['badge', getStatusBadge(application.status)]">
                {{ application.status }}
              </span>
            </template>
            <template v-else-if="column.key === 'application_date'">
              {{ formatDate(application[column.key]) }}
            </template>
            <template v-else>
              {{ getNestedValue(application, column.key) }}
            </template>
          </td>
          <td v-if="showActions">
            <slot name="actions" :application="application"></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const props = defineProps({
  applications: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  showActions: {
    type: Boolean,
    default: false
  },
  emptyMessage: {
    type: String,
    default: 'No applications found'
  }
})

const getNestedValue = (obj, path) => {
  return path.split('.').reduce((current, key) => current?.[key], obj) || '-'
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getStatusBadge = (status) => {
  switch (status?.toLowerCase()) {
    case 'applied':
      return 'bg-primary'
    case 'shortlisted':
      return 'bg-info'
    case 'selected':
      return 'bg-success'
    case 'rejected':
      return 'bg-danger'
    default:
      return 'bg-secondary'
  }
}
</script>

<style scoped>
.table {
  margin-bottom: 0;
}

.table thead th {
  font-weight: 600;
  border-bottom: 2px solid #dee2e6;
}

.table tbody tr {
  transition: background-color 0.2s;
}

.table tbody tr:hover {
  background-color: #f8f9fa;
}
</style>
