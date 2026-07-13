<template>
  <div class="dashboard-layout">
    <Navbar />
    <div class="dashboard-container">
      <div class="container py-4">
        <router-view />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.dashboard-container {
  flex: 1;
}
</style>
