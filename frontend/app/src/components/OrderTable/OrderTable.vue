<template>
    <div class="table-wrap" :class="{ flipped: isFlipped }">
        <div class="front side">
            <table>
                <caption>
                    <span v-if="tgUsername">{{ tgUsername }}</span>
                </caption>
                <thead>
                    <tr>
                        <th scope="col">
                            <p>Монета</p>
                        </th>
                        <th scope="col">
                            <p>Количество</p>
                        </th>
                        <th scope="col">
                            <p>Статус</p>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <!-- Динамическое отображение ордеров -->
                    <tr
                        @click="handleRowClick(order)"
                        v-for="order in orders"
                        :key="order.id"
                        tabindex="0"
                    >
                        <th scope="row">
                            <p>{{ order.coinName }}({{ order.coinTicker }})</p>
                        </th>
                        <td>
                            <p>{{ order.coinAmount }}</p>
                        </td>
                        <td>
                            <span>{{ order.status }}</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div class="back side">
            <button @click="goBack">Назад</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getAllOrders } from "./utils";


const tgUsername = ref(null);
const orders = ref([]);
const isFlipped = ref(false);   // Состояние для переключения анимации


// Извлекаем данные пользователя из localStorage и получаем ордера
onMounted(async () => {
    const userData = localStorage.getItem("user");
    tgUsername.value = userData ? JSON.parse(userData).tgUsername : null;

    orders.value = await getAllOrders();
});


// Функция для обработки клика на строку
function handleRowClick(order) {
    // alert(`Вы кликнули на ордер ${order.id}`);
    isFlipped.value = !isFlipped.value;
}

// Обработка кнопки "Назад"
function goBack() {
    isFlipped.value = false;
}

</script>

<style lang="scss" scoped>
@use "./style.scss";
</style>