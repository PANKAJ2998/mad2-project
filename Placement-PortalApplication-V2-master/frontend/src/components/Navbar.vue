<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        <strong>Placement Portal</strong>
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        @click="toggleNav"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div :class="['collapse', 'navbar-collapse', { show: isNavOpen }]">
        <ul class="navbar-nav ms-auto">
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register/student" class="nav-link">Student Register</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register/company" class="nav-link">Company Register</router-link>
            </li>
          </template>

          <template v-else>
            <li class="nav-item" v-if="authStore.isStudent">
              <router-link to="/student/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="authStore.isStudent">
              <router-link to="/student/drives" class="nav-link">Browse Drives</router-link>
            </li>
            <li class="nav-item" v-if="authStore.isStudent">
              <router-link to="/student/applications" class="nav-link">My Applications</router-link>
            </li>

            <li class="nav-item" v-if="authStore.isCompany">
              <router-link to="/company/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="authStore.isCompany">
              <router-link to="/company/create-drive" class="nav-link">Create Drive</router-link>
            </li>

            <li class="nav-item" v-if="authStore.isAdmin">
              <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="authStore.isAdmin">
              <router-link to="/admin/companies" class="nav-link">Manage Companies</router-link>
            </li>
            <li class="nav-item" v-if="authStore.isAdmin">
              <router-link to="/admin/drives" class="nav-link">Manage Drives</router-link>
            </li>

            <li class="nav-item">
              <a href="#" class="nav-link" @click.prevent="handleLogout">Logout</a>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()
const isNavOpen = ref(false)

const toggleNav = () => {
  isNavOpen.value = !isNavOpen.value
}

const handleLogout = () => {
  authStore.logout()
  isNavOpen.value = false
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  padding: 0.5rem 1rem;
  transition: color 0.3s;
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.8);
}
</style>
