<template>
  <div class="card stats-card h-100">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start">
        <div>
          <h6 class="card-subtitle text-muted mb-2">{{ title }}</h6>
          <h2 class="card-title mb-0">{{ value }}</h2>
          <p class="text-muted small mt-2" v-if="subtitle">{{ subtitle }}</p>
        </div>
        <div :class="['icon-wrapper', iconColorClass]">
          <i :class="icon"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: 'bi bi-graph-up'
  },
  iconColor: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'danger', 'info'].includes(value)
  }
})

const iconColorClass = `bg-${props.iconColor}`
</script>

<style scoped>
.stats-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stats-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
}

.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.2;
}

.icon-wrapper i {
  font-size: 24px;
  color: white;
}
</style>
