import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/trip-plan/create',
    },
    {
      path: '/trip-plan/create',
      name: 'createTripPlan',
      component: () => import('@/views/CreateTripPlanView.vue'),
    },
    {
      path: '/trip-plan/:userId',
      name: 'tripPlanDetail',
      component: () => import('@/views/TripPlanDetailView.vue'),
    },
    {
      path: '/trip-plan/update/:userId',
      name: 'updateTripPlan',
      component: () => import('@/views/UpdateTripPlanView.vue'),
    },
  ],
})

export default router
