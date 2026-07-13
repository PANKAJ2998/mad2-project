import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'

import LandingPage from '@/views/LandingPage.vue'

import AuthLayout from '@/layouts/AuthLayout.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'

import Login from '@/views/auth/Login.vue'
import StudentRegister from '@/views/auth/StudentRegister.vue'
import CompanyRegister from '@/views/auth/CompanyRegister.vue'

import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import ManageCompanies from '@/views/admin/ManageCompanies.vue'
import ManageDrives from '@/views/admin/ManageDrives.vue'

import CompanyDashboard from '@/views/company/CompanyDashboard.vue'
import CreateDrive from '@/views/company/CreateDrive.vue'
import DriveApplications from '@/views/company/DriveApplications.vue'

import StudentDashboard from '@/views/student/StudentDashboard.vue'
import BrowseDrives from '@/views/student/BrowseDrives.vue'
import MyApplications from '@/views/student/MyApplications.vue'
import StudentProfile from '@/views/student/StudentProfile.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/login',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: Login
      }
    ]
  },
  {
    path: '/register',
    component: AuthLayout,
    children: [
      {
        path: 'student',
        name: 'StudentRegister',
        component: StudentRegister
      },
      {
        path: 'company',
        name: 'CompanyRegister',
        component: CompanyRegister
      }
    ]
  },
  {
    path: '/admin',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'companies',
        name: 'ManageCompanies',
        component: ManageCompanies
      },
      {
        path: 'drives',
        name: 'ManageDrives',
        component: ManageDrives
      }
    ]
  },
  {
    path: '/company',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'company' },
    children: [
      {
        path: 'dashboard',
        name: 'CompanyDashboard',
        component: CompanyDashboard
      },
      {
        path: 'create-drive',
        name: 'CreateDrive',
        component: CreateDrive
      },
      {
        path: 'drive-applications/:id',
        name: 'DriveApplications',
        component: DriveApplications
      }
    ]
  },
  {
    path: '/student',
    component: DashboardLayout,
    meta: { requiresAuth: true, role: 'student' },
    children: [
      {
        path: 'dashboard',
        name: 'StudentDashboard',
        component: StudentDashboard
      },
      {
        path: 'drives',
        name: 'BrowseDrives',
        component: BrowseDrives
      },
      {
        path: 'applications',
        name: 'MyApplications',
        component: MyApplications
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: StudentProfile
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()
  const userRole = authService.getRole()

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' })
    } else if (to.meta.role && to.meta.role !== userRole) {
      if (userRole === 'admin') {
        next({ name: 'AdminDashboard' })
      } else if (userRole === 'company') {
        next({ name: 'CompanyDashboard' })
      } else if (userRole === 'student') {
        next({ name: 'StudentDashboard' })
      } else {
        next({ name: 'Landing' })
      }
    } else {
      next()
    }
  } else if ((to.name === 'Login' || to.name === 'StudentRegister' || to.name === 'CompanyRegister') && isAuthenticated) {
    if (userRole === 'admin') {
      next({ name: 'AdminDashboard' })
    } else if (userRole === 'company') {
      next({ name: 'CompanyDashboard' })
    } else if (userRole === 'student') {
      next({ name: 'StudentDashboard' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
