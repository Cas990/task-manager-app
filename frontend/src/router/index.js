import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../views/LoginPage.vue';
import TaskPage from '../views/TaskPage.vue';

const routes = [
  { path: '/', component: LoginPage },
  { path: '/tasks', component: TaskPage, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to protect routes that require authentication
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !localStorage.getItem('user')) {
    next('/');
  } else {
    next();
  }
});

export default router;
