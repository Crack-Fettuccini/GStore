import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/PrelogViews/homeView.vue'
import PrelogView from '@/views/StateViews/PrelogView.vue'
import PostlogView from '@/views/StateViews/PostlogView.vue'
import userItemsView from  '@/views/UserViews/itemsView.vue'
import managerItemsView from  '@/views/ManagerViews/itemsView.vue'
import adminCategoryView from  '@/views/AdminViews/categoryView.vue'

const routes = [
  {
    path: '/',
    component: PrelogView,
    children: [
      {path: '', name: 'homeView',component: HomeView},
      {path: 'about', name: 'aboutView',component: () => import('@/views/PrelogViews/aboutView.vue')},
      {path: 'login', name: 'loginView', component: () => import('@/views/PrelogViews/loginView.vue')},
      {path: 'register', name: 'registerView', component: () => import( '@/views/PrelogViews/registrationView.vue')},
    ],
    meta: { requiresAuth: false}
  },
  {
    path: '/user',
    component: PostlogView,
    children: [
      {path: 'dashboard', name: 'userItemsView',component: userItemsView},
      {path: 'profile', name: 'userProfileView',component: () => import ('@/views/UserViews/profileView.vue')},
      {path: 'orders', name: 'userOrdersView',component: () => import ('@/views/UserViews/ordersView.vue')},
      {path: 'checkout', name: 'userCheckoutView',component: () => import ('@/views/UserViews/checkoutView.vue')},
    ],
    meta: { requiresAuth: true, level: 'user' }
  },
  {
    path: '/manager',
    component: PostlogView,
    children: [
      {path: 'dashboard', name: 'managerItemsView',component: managerItemsView},
      {path: 'profile', name: 'managerProfileView',component: () => import ('@/views/UserViews/profileView.vue')},
      {path: 'tickets', name: 'managerTicketView',component: () => import ('@/views/ManagerViews/ticketView.vue')},
    ],
    meta: { requiresAuth: true, level: 'manager' }
  },

  {
    path: '/admin',
    component: PostlogView,
    children: [
      {path: 'dashboard', name: 'adminItemsView',component: adminCategoryView},
      {path: 'profile', name: 'adminProfileView',component: () => import ('@/views/UserViews/profileView.vue')},
      {path: 'tickets', name: 'adminTicketView',component: () => import ('@/views/AdminViews/ticketView.vue')},
      {path: 'requests', name: 'adminRequestView',component: () => import ('@/views/AdminViews/requestView.vue')},
    ],
    meta: { requiresAuth: true, level: 'admin' }
  },
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
