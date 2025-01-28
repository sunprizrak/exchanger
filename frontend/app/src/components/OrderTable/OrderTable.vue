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
                        v-for="order in userStore.orders"
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
            <div v-if="selectedOrder" class="order-details">
                <span>Детали ордера</span>
                <p v-if="tgUsername"><strong>Пользователь:</strong> {{ tgUsername }}</p>
                <p><strong>Монета:</strong> {{ selectedOrder.coinName }} ({{ selectedOrder.coinTicker }})</p>
                <p><strong>Количество:</strong> {{ selectedOrder.coinAmount }}</p>
                <p><strong>Валюта:</strong> {{ selectedOrder.currency}} ({{ selectedOrder.currencyCode }})</p>
                <p><strong>Способ оплаты:</strong> {{ selectedOrder.paymentMethod }}</p>
                <p><strong>Стоимость:</strong> {{ selectedOrder.totalPrice }}</p>
                <p><strong>Статус:</strong> <span>{{ selectedOrder.status }}</span></p>
                <p><strong>Создан:</strong> {{ selectedOrder.createdFormatted }}</p>
                <!-- Добавьте другие свойства, если нужно -->
            </div>
            <div class="box-input">
                <input
                    type="text"
                    placeholder="Ваш кошелек"
                />

            </div>
            <input type="file" />
            <button @click="goBack">Назад</button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue";
import { useUserStore } from "@/stores/user";


// <<<STORES>>>
const userStore = useUserStore();

// <<<STATES>>>
const tgUsername = ref(null);
const isFlipped = ref(false);        // Состояние для переключения анимации
const selectedOrder = ref(null);


// Извлекаем данные пользователя из localStorage и получаем ордера
onMounted(async () => {
    const userData = localStorage.getItem("user");
    tgUsername.value = userData ? JSON.parse(userData).tgUsername : null;

    await userStore.loadOrders();

    // Запускаем полинг при монтировании компонента
    await userStore.startOrderStatusPolling();
});

onUnmounted(() => {
    // Останавливаем полинг при размонтировании компонента
    userStore.stopOrderStatusPolling();
});

// Функция для обработки клика на строку
function handleRowClick(order) {
    selectedOrder.value = order;          // Сохраняем выбранный ордер
    isFlipped.value = !isFlipped.value;
}

// Обработка кнопки "Назад"
function goBack() {
    isFlipped.value = false;
    selectedOrder.value = null;            // Сбрасываем выбранный ордер
}

</script>

<style lang="scss" scoped>
@use "./style.scss";
</style>