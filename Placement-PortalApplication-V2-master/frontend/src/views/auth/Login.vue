<template>
  <div class="login-card card shadow">
    <div class="card-body p-4">
      <h3 class="text-center mb-4">Login</h3>

      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}
        <button type="button" class="btn-close" @click="error = null"></button>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            v-model="form.email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="form.password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="authStore.loading">
          <span v-if="authStore.loading">
            <span class="spinner-border spinner-border-sm me-2"></span>
            Logging in...
          </span>
          <span v-else>Login</span>
        </button>
      </form>

      <hr class="my-4" />

      <p class="text-center text-muted mb-2">Don't have an account?</p>
      <div class="d-grid gap-2">
        <router-link to="/register/student" class="btn btn-outline-primary">
          Register as Student
        </router-link>
        <router-link to="/register/company" class="btn btn-outline-success">
          Register as Company
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: ''
})

const error = ref(null)

const handleLogin = async () => {
  error.value = null
  try {
    await authStore.login(form.value)

    if (authStore.isAdmin) {
      router.push('/admin/dashboard')
    } else if (authStore.isCompany) {
      router.push('/company/dashboard')
    } else if (authStore.isStudent) {
      router.push('/student/dashboard')
    }
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed. Please try again.'
  }
}
</script>

<style scoped>
.login-card {
  border: none;
  margin-top: 2rem;
}
</style>
