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
            <div id='backButton'>
                <div :class="{'active-click': isActiveBackButton}" @click="handleBackButton">
                    лол
                </div>
            </div>
            <div v-if="selectedOrder" class="order-details">
                <span>Детали ордера</span>
                <p v-if="tgUsername"><strong>Пользователь:</strong> {{ tgUsername }}</p>
                <p><strong>Монета:</strong> {{ selectedOrder.coinName }} ({{ selectedOrder.coinTicker }})</p>
                <p><strong>Количество:</strong> {{ selectedOrder.coinAmount }}</p>
                <p><strong>Способ оплаты:</strong> {{ selectedOrder.paymentMethod }}</p>
                <p><strong>Валюта:</strong> {{ selectedOrder.currency}} ({{ selectedOrder.currencyCode }})</p>
                <p><strong>Стоимость:</strong> {{ selectedOrder.totalPrice }}</p>
                <p><strong>Статус:</strong> <span>{{ selectedOrder.status }}</span></p>
                <p><strong>Создан:</strong> {{ selectedOrder.createdFormatted }}</p>
                <!-- Добавьте другие свойства, если нужно -->
            </div>
            <div class="box-input">
                <textarea
                    type="text"
                    placeholder="Введите сюда ваш кошелёк"
                />

            </div>
            <div id='bottom-line'>
                <div id="foto-check-input">
                    <label for="dropzone-file" class="flex flex-col items-center justify-center border-2 border-dashed rounded-lg cursor-pointer">
                        <div class="flex flex-col items-center justify-center">
                            <svg class="w-8 h-8" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 16">
                                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"/>
                            </svg>
                            <p>
                                Фото чека<br>
                                c оплатой
                            </p>
                        </div>
                        <input id="dropzone-file" type="file" class="hidden" />
                    </label>
                </div>
                <div id="uploaded-img">
                    <img   alt="foto-check-img" />
                </div>
                <div id="order-pay-button">
                    <div :class="{'active-click': isActiveOrderPayButton}" @click="handleOrderPaySubmit">Оплатил</div>
                </div>
            </div>
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
const isActiveOrderPayButton = ref(false);
const isActiveBackButton = ref(false);

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
const handleBackButton = async () => {
    isActiveBackButton.value = true;


    // Убираем активный класс через 300ms (время длительности анимации)
    setTimeout(() => {
        isActiveBackButton.value = false;
    }, 300);

    const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
    await sleep(500);

    isFlipped.value = false;
    selectedOrder.value = null;           // Сбрасываем выбранный ордер
};

// Обработка клика кнопки OrderPayButton
const handleOrderPaySubmit = async () => {
    isActiveOrderPayButton.value = true;

    // Убираем активный класс через 300ms (время длительности анимации)
    setTimeout(() => {
        isActiveOrderPayButton.value = false;
    }, 300);
};

</script>

<style lang="scss" scoped>
@use "./style.scss";
</style>