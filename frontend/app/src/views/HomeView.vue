<script setup>

</script>

<template>
    <main>
        <div>
            <h1>Telegram WebApp Example</h1>
            <div v-if="telegramData">
                <p><strong>id:</strong> {{ tgId }}</p>
                <p><strong>username:</strong> {{ tgUsername }}</p>
            </div>
            <div v-else>
                <p>Данные Telegram WebApp не получены.</p>
            </div>
        </div>
    </main>
</template>


<script>

</script>