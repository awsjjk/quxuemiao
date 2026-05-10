import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/login', name: 'Login', component: () => import('../views/LoginPage.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterPage.vue') },
  {
    path: '/dashboard', name: 'Dashboard',
    component: () => import('../views/DashboardPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/demand/:id', name: 'DemandDetail',
    component: () => import('../views/DemandDetailPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/match/:demand_id', name: 'MatchResult',
    component: () => import('../views/MatchResultPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/select-demand', name: 'SelectDemand',
    component: () => import('../views/SelectDemandPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/order/:id', name: 'OrderDetail',
    component: () => import('../views/OrderDetailPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/profile', name: 'Profile',
    component: () => import('../views/ProfilePage.vue'),
    meta: { auth: true }
  },
  {
    path: '/messages', name: 'Messages',
    component: () => import('../views/MessagePage.vue'),
    meta: { auth: true }
  },
  {
    path: '/messages/:partner_id', name: 'Chat',
    component: () => import('../views/MessagePage.vue'),
    meta: { auth: true }
  },
  {
    path: '/resources', name: 'Resources',
    component: () => import('../views/ResourcePage.vue'),
    meta: { auth: true }
  },
  {
    path: '/payments', name: 'Payments',
    component: () => import('../views/PaymentPage.vue'),
    meta: { auth: true }
  },
  {
    path: '/ai-assistant', name: 'AIAssistant',
    component: () => import('../views/AIAssistantPage.vue'),
    meta: { auth: true }
  },
  { path: '/', redirect: '/dashboard' },
  { path: '/:pathMatch(.*)', redirect: '/dashboard' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.auth && !auth.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router
