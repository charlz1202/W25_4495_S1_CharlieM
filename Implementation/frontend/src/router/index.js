import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import LoginPage from '../views/LoginPage.vue';
import SignupPage from '../views/SignupPage.vue';
import Dashboard from '../views/Dashboard.vue';
import PetProfile from '../views/PetProfile.vue';


const routes = [
    {path : '/', component: HomePage},
    {path : '/login', component: LoginPage},
    {path : '/signup', component: SignupPage},
    {path : '/dashboard', component: Dashboard, meta: {requiresAuth: true}},
    { path: "/pets/:id", name: "PetProfile", component: PetProfile },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;