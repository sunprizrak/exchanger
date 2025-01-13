import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import OrdersView from '@/views/OrdersView.vue'
import CoinsView from '@/views/CoinsView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/orders',
            name: 'orders',
            component: OrdersView,
        },
        {
            path: '/coins',
            name: 'coins',
            component: CoinsView,
        },

    ],
})

export default router
