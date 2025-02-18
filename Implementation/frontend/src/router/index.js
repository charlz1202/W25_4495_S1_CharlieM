import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../views/LoginPage.vue';
import SignupPage from '../views/SignupPage.vue';
import Dashboard from '../views/Dashboard.vue';
import PetProfile from '../views/PetProfile.vue';

const routes = [
    {path : '/', redirect: "/login"},
    {path : '/login', component: LoginPage},
    {path : '/signup', component: SignupPage},
    {
        path : '/dashboard',
        component: Dashboard,
        meta: {requiresAuth: true}
    },
    { path: "/pets/:id", name: "PetProfile", component: PetProfile }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem("token");
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    }  else {
        next();
    }
});

export default router;