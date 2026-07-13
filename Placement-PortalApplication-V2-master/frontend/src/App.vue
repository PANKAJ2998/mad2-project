<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>
@import 'bootstrap/dist/css/bootstrap.min.css';
@import 'bootstrap-icons/font/bootstrap-icons.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f8f9fa;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.card {
  border-radius: 8px;
}

.btn {
  border-radius: 6px;
}

.form-control,
.form-select {
  border-radius: 6px;
}

.badge {
  font-weight: 500;
  padding: 0.35em 0.65em;
}

a {
  text-decoration: none;
}

.router-link-active {
  font-weight: 600;
}
</style>
