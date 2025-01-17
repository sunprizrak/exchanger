import { createApp, onMounted } from 'vue';
import App from './App.vue';
import './index.css';
import 'flowbite';
import router from './router';
import { apolloProvider } from "@/apollo-config";
import { createPinia } from "pinia";
import { telegramUtils, initializeTelegram } from '@/services/telegram';
import { telegramAuth } from '@/services/auth';
import { useCoinsStore } from "@/stores/coin";
import { useCurrenciesStore } from "@/stores/currency";


async function main() {
    try {
        // Создание Vue приложения
        createVueApp();

        const coinsStore = useCoinsStore();
        await coinsStore.loadCoins(); // Загружаем монеты

        const currenciesStore = useCurrenciesStore();
        await currenciesStore.loadCurrencies(); // Загружаем валюты

        // Проверка на запуск внутри Telegram WebApp
        if (telegramUtils.isTelegramWebApp) {
            // Инициализация Telegram данных
            const initData = await initializeTelegram();
            // Авторизация через Telegram
            await telegramAuth(initData);
        } else {
            console.warn("Приложение не запущено внутри Telegram WebApp.");
        }
    } catch (error) {
        console.error("Ошибка при инициализации приложения:", error);
    }
}

// Функция для создания Vue приложения
function createVueApp() {
    const app = createApp(App)

    app.use(createPinia())
        .use(router)
        .use(apolloProvider)
        .mount("#app");
}


main();





