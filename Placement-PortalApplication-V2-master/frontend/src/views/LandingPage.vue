<template>
  <div class="landing-page">
    <Navbar />

    <section class="hero-section">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <h1 class="display-4 fw-bold mb-4">Welcome to Placement Portal</h1>
            <p class="lead mb-4">
              Connecting students, companies, and institutes for successful campus placements.
              Streamline your placement process with our comprehensive platform.
            </p>
            <div class="cta-buttons d-flex justify-content-center gap-3 flex-wrap">
              <router-link to="/login" class="btn btn-primary btn-lg">
                Login
              </router-link>
              <router-link to="/register/student" class="btn btn-outline-light btn-lg">
                Register as Student
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="features-section py-5">
      <div class="container">
        <h2 class="text-center mb-5">Platform Features</h2>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card text-center p-4">
              <div class="feature-icon mb-3">
                <i class="bi bi-speedometer2 display-4 text-primary"></i>
              </div>
              <h4>Easy Management</h4>
              <p class="text-muted">
                Manage placement drives, applications, and student profiles effortlessly.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card text-center p-4">
              <div class="feature-icon mb-3">
                <i class="bi bi-shield-check display-4 text-success"></i>
              </div>
              <h4>Secure & Reliable</h4>
              <p class="text-muted">
                Enterprise-grade security with role-based access control.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="feature-card text-center p-4">
              <div class="feature-icon mb-3">
                <i class="bi bi-graph-up display-4 text-info"></i>
              </div>
              <h4>Real-time Analytics</h4>
              <p class="text-muted">
                Track applications, selections, and placement statistics in real-time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="roles-section py-5 bg-light">
      <div class="container">
        <h2 class="text-center mb-5">Who Can Use</h2>
        <div class="row g-4">
          <div class="col-lg-4">
            <div class="role-card card h-100">
              <div class="card-body">
                <div class="role-icon mb-3">
                  <i class="bi bi-person-badge display-3 text-primary"></i>
                </div>
                <h4 class="card-title">Students</h4>
                <ul class="list-unstyled text-muted">
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Browse placement drives</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Apply to eligible drives</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Track application status</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Manage profile</li>
                </ul>
                <router-link to="/register/student" class="btn btn-outline-primary w-100 mt-3">
                  Register Now
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-lg-4">
            <div class="role-card card h-100">
              <div class="card-body">
                <div class="role-icon mb-3">
                  <i class="bi bi-building display-3 text-success"></i>
                </div>
                <h4 class="card-title">Companies</h4>
                <ul class="list-unstyled text-muted">
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Create placement drives</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>View applications</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Shortlist candidates</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Update application status</li>
                </ul>
                <router-link to="/register/company" class="btn btn-outline-success w-100 mt-3">
                  Register Company
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-lg-4">
            <div class="role-card card h-100">
              <div class="card-body">
                <div class="role-icon mb-3">
                  <i class="bi bi-person-gear display-3 text-info"></i>
                </div>
                <h4 class="card-title">Admin</h4>
                <ul class="list-unstyled text-muted">
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Approve companies</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Approve placement drives</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>View analytics</li>
                  <li><i class="bi bi-check-circle-fill text-success me-2"></i>Manage platform</li>
                </ul>
                <router-link to="/login" class="btn btn-outline-info w-100 mt-3">
                  Admin Login
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="how-it-works py-5">
      <div class="container">
        <h2 class="text-center mb-5">How It Works</h2>
        <div class="row g-4">
          <div class="col-md-3 text-center">
            <div class="step-badge mb-3">1</div>
            <h5>Register</h5>
            <p class="text-muted">Create your account as student or company</p>
          </div>
          <div class="col-md-3 text-center">
            <div class="step-badge mb-3">2</div>
            <h5>Get Approved</h5>
            <p class="text-muted">Admin reviews and approves your account</p>
          </div>
          <div class="col-md-3 text-center">
            <div class="step-badge mb-3">3</div>
            <h5>Browse/Create Drives</h5>
            <p class="text-muted">Students apply, companies create drives</p>
          </div>
          <div class="col-md-3 text-center">
            <div class="step-badge mb-3">4</div>
            <h5>Track Progress</h5>
            <p class="text-muted">Monitor applications and selections</p>
          </div>
        </div>
      </div>
    </section>

    <Footer />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
.hero-section {
  padding: 80px 0 60px;
  background: linear-gradient(135deg, #1b2550 0%, #150822 100%);
  color: white;
}

.hero-section h1 {
  color: white;
}

.hero-section .lead {
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.25rem;
}

.hero-section .btn-outline-light {
  border-color: white;
  color: white;
}

.hero-section .btn-outline-light:hover {
  background-color: white;
  color: #667eea;
}

.hero-image img {
  max-height: 500px;
  object-fit: cover;
  width: 100%;
}

.feature-card,
.role-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.feature-card:hover,
.role-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.step-badge {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 0 30px;
  }

  .hero-section .lead {
    font-size: 1.1rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .cta-buttons .btn {
    width: 100%;
  }

  .hero-image img {
    max-height: 300px;
  }
}
</style>
