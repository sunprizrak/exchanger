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
import { initializeTelegram, telegramAuth } from '@/services/telegram';
import { useUserStore } from '@/stores/user';

onMounted(async () => {
    const userStore = useUserStore();

    // Инициализируем Telegram и получаем initData
    const initData = 'test'        // await initializeTelegram();

    // Авторизация через Telegram
    const { token, user } = await telegramAuth(initData);

    // Сохраняем данные в store
    userStore.setToken(token);
    userStore.setUser(user);
});


</script>

<style scoped>

</style>
