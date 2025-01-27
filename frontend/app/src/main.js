import { createApp } from 'vue';
import App from './App.vue';
import './index.css';
import 'flowbite';
import router from './router';
import { apolloProvider } from "@/apollo-config";
import { createPinia } from "pinia";
import Vue3Lottie from 'vue3-lottie';
import { useCoinsStore } from '@/stores/coin';
import { useCurrenciesStore } from '@/stores/currency';


async function main() {
    try {
        // Создание Vue приложения
        createVueApp();

        const coinsStore = useCoinsStore();
        const currenciesStore = useCurrenciesStore();

        await coinsStore.loadCoins(); // Загружаем монеты
        await currenciesStore.loadCurrencies(); // Загружаем валюты
    } catch (error) {
        console.error("Ошибка при инициализации приложения:", error.message);
    }
}

// Функция для создания Vue приложения
function createVueApp() {
    const app = createApp(App)

    app.use(createPinia())
        .use(Vue3Lottie)
        .use(router)
        .use(apolloProvider)
        .mount("#app");
}


main();





