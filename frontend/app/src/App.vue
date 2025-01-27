<template>
    <header>
        <Navbar />
    </header>

    <RouterView />
</template>

<script setup>
import { onMounted } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import { telegram, initializeTelegram, telegramAuth } from '@/services/telegram';
import { useUserStore } from '@/stores/user';

onMounted(async () => {
    const userStore = useUserStore();

    // Проверка на запуск внутри Telegram WebApp
    if (telegram.isWebApp) {
        // Инициализируем Telegram и получаем initData
        const initData = await initializeTelegram();

        // Авторизация через Telegram
        const { token, user } = await telegramAuth(initData);

        // Сохраняем данные в store
        userStore.setToken(token);
        userStore.setUser(user);

    } else {
        console.warn("Приложение не запущено внутри Telegram WebApp.");
    }
});


</script>

<style scoped>

</style>
