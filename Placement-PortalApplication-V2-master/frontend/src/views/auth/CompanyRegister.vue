<template>
  <div class="register-card card shadow">
    <div class="card-body p-4">
      <h3 class="text-center mb-4">Company Registration</h3>

      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}
        <button type="button" class="btn-close" @click="error = null"></button>
      </div>

      <div v-if="success" class="alert alert-success">
        Registration successful! Your account will be activated after admin approval.
      </div>

      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="company_name" class="form-label">Company Name</label>
          <input
            type="text"
            class="form-control"
            id="company_name"
            v-model="form.company_name"
            required
          />
        </div>

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
            minlength="6"
            required
          />
          <div class="form-text">Minimum 6 characters</div>
        </div>

        <div class="mb-3">
          <label for="hr_contact" class="form-label">HR Contact</label>
          <input
            type="text"
            class="form-control"
            id="hr_contact"
            v-model="form.hr_contact"
          />
        </div>

        <div class="mb-3">
          <label for="website" class="form-label">Website</label>
          <input
            type="url"
            class="form-control"
            id="website"
            v-model="form.website"
            placeholder="https://example.com"
          />
        </div>

        <div class="alert alert-info">
          <small>
            <i class="bi bi-info-circle me-2"></i>
            Your account will be reviewed by the admin before activation.
          </small>
        </div>

        <button type="submit" class="btn btn-success w-100" :disabled="authStore.loading">
          <span v-if="authStore.loading">
            <span class="spinner-border spinner-border-sm me-2"></span>
            Registering...
          </span>
          <span v-else>Register Company</span>
        </button>
      </form>

      <hr class="my-3" />

      <p class="text-center text-muted mb-0">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>
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
  company_name: '',
  email: '',
  password: '',
  hr_contact: '',
  website: ''
})

const error = ref(null)
const success = ref(false)

const handleRegister = async () => {
  error.value = null
  try {
    await authStore.registerCompany(form.value)
    success.value = true
    setTimeout(() => {
      router.push('/company/dashboard')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.message || 'Registration failed. Please try again.'
  }
}
</script>

<style scoped>
.register-card {
  border: none;
  margin-top: 2rem;
}
</style>
