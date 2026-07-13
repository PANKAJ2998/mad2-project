<template>
  <div class="register-card card shadow">
    <div class="card-body p-4">
      <h3 class="text-center mb-4">Student Registration</h3>

      <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ error }}
        <button type="button" class="btn-close" @click="error = null"></button>
      </div>

      <div v-if="success" class="alert alert-success">
        Registration successful! Redirecting...
      </div>

      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
          <input
            type="text"
            class="form-control"
            id="name"
            v-model="form.name"
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
          <label for="branch" class="form-label">Branch</label>
          <select class="form-select" id="branch" v-model="form.branch" required>
            <option value="">Select Branch</option>
            <option value="CSE">Computer Science</option>
            <option value="ECE">Electronics</option>
            <option value="EEE">Electrical</option>
            <option value="MECH">Mechanical</option>
            <option value="CIVIL">Civil</option>
          </select>
        </div>

        <div class="mb-3">
          <label for="cgpa" class="form-label">CGPA</label>
          <input
            type="number"
            class="form-control"
            id="cgpa"
            v-model.number="form.cgpa"
            step="0.01"
            min="0"
            max="10"
            required
          />
        </div>

        <div class="mb-3">
          <label for="graduation_year" class="form-label">Graduation Year</label>
          <input
            type="number"
            class="form-control"
            id="graduation_year"
            v-model.number="form.graduation_year"
            min="2024"
            max="2030"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100" :disabled="authStore.loading">
          <span v-if="authStore.loading">
            <span class="spinner-border spinner-border-sm me-2"></span>
            Registering...
          </span>
          <span v-else">Register</span>
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
  name: '',
  email: '',
  password: '',
  branch: '',
  cgpa: '',
  graduation_year: new Date().getFullYear()
})

const error = ref(null)
const success = ref(false)

const handleRegister = async () => {
  error.value = null
  try {
    await authStore.registerStudent(form.value)
    success.value = true
    setTimeout(() => {
      router.push('/student/dashboard')
    }, 1500)
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
