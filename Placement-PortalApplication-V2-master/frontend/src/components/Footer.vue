<template>
  <footer class="bg-dark text-white py-4 mt-5">
    <div class="container">
      <div class="row">
        <div class="col-md-4 mb-3 mb-md-0">
          <h5>Placement Portal</h5>
          <p class="text-white-50">Connecting students, companies, and institutes for successful placements.</p>
        </div>
        <div class="col-md-4 mb-3 mb-md-0">
          <h5>Quick Links</h5>
          <ul class="list-unstyled">
            <li><router-link to="/" class="text-white-50 text-decoration-none">Home</router-link></li>
            <li><router-link to="/login" class="text-white-50 text-decoration-none">Login</router-link></li>
            <li><a href="#" class="text-white-50 text-decoration-none">About</a></li>
            <li><a href="#" class="text-white-50 text-decoration-none">Contact</a></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h5>Contact</h5>
          <p class="text-white-50 mb-1">Email: placement@institute.edu</p>
          <p class="text-white-50">Phone: (555) 123-4567</p>
        </div>
      </div>
      <hr class="bg-secondary my-3" />
      <div class="text-center text-white-50">
        <p class="mb-0">&copy; 2026 Placement Portal. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
footer {
  margin-top: auto;
}

footer a:hover {
  color: white !important;
}
</style>
