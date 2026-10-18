import { createRouter, createWebHistory } from 'vue-router'
import { authState, isAdmin } from '../utils/auth'

const routes = [
  {
    path: '/',
    component: () => import('../components/StoreLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('../views/HomeView.vue') },
      { path: 'catalog', name: 'catalog', component: () => import('../views/CatalogView.vue') },
      { path: 'orders', name: 'my-orders', component: () => import('../views/MyOrdersView.vue'), meta: { requiresAuth: true } },
      { path: 'addresses', name: 'my-addresses', component: () => import('../views/MyAddressesView.vue'), meta: { requiresAuth: true } },
      { path: 'profile', name: 'profile', component: () => import('../views/ProfileView.vue'), meta: { requiresAuth: true } }
    ]
  },
  { path: '/login', name: 'login', component: () => import('../views/LoginView.vue') },
  {
    path: '/admin',
    component: () => import('../components/AdminLayout.vue'),
    meta: { requiresAuth: true, admin: true },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('../views/admin/DashboardView.vue') },
      { path: 'goods', name: 'admin-goods', component: () => import('../views/admin/GoodsView.vue') },
      { path: 'categories', name: 'admin-categories', component: () => import('../views/admin/CategoriesView.vue') },
      { path: 'orders', name: 'admin-orders', component: () => import('../views/admin/OrdersView.vue') },
      { path: 'users', name: 'admin-users', component: () => import('../views/admin/UsersView.vue') },
      { path: 'addresses', name: 'admin-addresses', component: () => import('../views/admin/AddressesView.vue') },
      { path: 'notices', name: 'admin-notices', component: () => import('../views/admin/NoticesView.vue') }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !authState.user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.admin && !isAdmin()) {
    return { name: 'home' }
  }
  if (to.name === 'login' && authState.user) {
    return isAdmin() ? { name: 'admin-dashboard' } : { name: 'home' }
  }
  return true
})

export default router