<template>
  <div class="auth-layout">
    <Navbar />
    <div class="auth-container">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-6 col-lg-5">
            <router-view />
          </div>
        </div>
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
.auth-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f5f5;
}

.auth-container {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 2rem 0;
}
</style>
