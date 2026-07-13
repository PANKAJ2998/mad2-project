<template>
  <div class="loader-container" v-if="loading">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
    <p class="mt-3 text-muted" v-if="message">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  loading: {
    type: Boolean,
    default: true
  },
  message: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 2rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
