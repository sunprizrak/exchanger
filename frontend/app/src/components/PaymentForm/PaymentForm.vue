<template>
    <div v-if="formVisible" class="form-wrap">
        <form>
            <div class="amount-input">
                <span>Вы отправляете</span>
                <div class="bottom-line">
                    <div class="country">
                        <img v-if="selectedCurrency" :src="selectedCurrency.fullIconUrl" alt="Currency Icon" />
                        <div>
                            <select v-model="selectedCode">
                                <option
                                    v-for="currency in currencies"
                                    :key="currency.code"
                                    :value="currency.code"
                                >
                                    {{ currency.code }}
                                </option>
                            </select>
                            <span v-if="selectedCurrency">{{ selectedCurrency.name }}</span>
                        </div>
                    </div>
                    <div class="box-input">
                        <input
                            type="text"
                            v-model="amountCurrency"
                            @input="validateCurrencyInput"
                            :min="minAmountCurrency"
                            :max="maxAmountCurrency"
                            placeholder="Введите сумму"
                            required
                        />
                        <p class="error" v-if="!isValidCurrency">
                            <span v-if="amountCurrency < minAmountCurrency">min: {{ selectedCurrency.symbol }}{{ minAmountCurrency.toFixed(2) }}</span>
                            <span v-else-if="amountCurrency > maxAmountCurrency">max: {{ selectedCurrency.symbol }}{{ maxAmountCurrency.toFixed(2) }}</span>
                        </p>
                        <!-- Отображение ошибки, если поле пустое -->
                        <p class="error" v-else-if="isSubmitted && amountCurrency === ''">
                            <span>Обязательное поле</span>
                        </p>
                    </div>
                </div>
            </div>
            <hr/>
            <div class="amount-input">
                <span>Вы получаете</span>
                <div class="bottom-line">
                    <div class="coins">
                        <img v-if="selectedCoin" :src="selectedCoin.fullIconUrl" alt="Coin Icon" />
                        <div>
                            <select v-model="selectedTicker">
                                <option
                                    v-for="coin in coins"
                                    :key="coin.ticker"
                                    :value="coin.ticker"
                                >
                                    {{ coin.ticker }}
                                </option>
                            </select>
                            <span v-if="selectedCoin">{{ selectedCoin.name }}</span>
                        </div>
                    </div>
                    <div class="box-input">
                        <input
                            type="text"
                            v-model="amountCoins"
                            @input="validateCoinsInput"
                            :min="minAmountCoins"
                            :max="maxAmountCoins"
                            placeholder="количество"
                        />
                        <p class="error" v-if="!isValidCoins">
                            <span v-if="amountCoins < minAmountCoins">min: {{ minAmountCoins.toFixed(8) }}</span>
                            <span v-else-if="amountCoins > maxAmountCoins">max: {{ maxAmountCoins.toFixed(8) }}</span>
                        </p>
                        <p class="error" v-else-if="isSubmitted && amountCoins === ''">
                            <span>Обязательное поле</span>
                        </p>
                    </div>
                </div>
            </div>
            <hr/>
            <div v-if="selectedCurrency && selectedCurrency.paymentMethods.length > 0" class="payment-methods">
                <span>Методы оплаты</span>
                <ul>
                    <li v-for="method in selectedCurrency.paymentMethods" :key="method.id">
                        <label>
                            <input
                                type="radio"
                                :value="method.id"
                                v-model="selectedPaymentMethod"
                            />
                            <span :class="{ active: selectedPaymentMethod === method.id }">{{ method.name }}</span>
                        </label>
                    </li>
                </ul>
                <p class="error" v-if="isSubmitted && selectedPaymentMethod === null">
                    <span>Обязательное поле</span>
                </p>
            </div>
        </form>
        <div class="form-button cst-btn">
            <div :class="{'active-click': isActivePayButton}" @click="handleSubmit">КУПИТЬ</div>
        </div>
    </div>
    <div v-if="animationVisible">
        <Vue3Lottie
            :animation-data="animHandshake"
            id="animHandshake"
            @on-loop-complete="onAnimationFinish"
        />
    </div>
</template>


<script setup>
import { computed, ref, watchEffect, watch } from "vue";
import { useCoinsStore } from "@/stores/coin";
import { useCurrenciesStore } from "@/stores/currency";
import debounce from 'lodash.debounce';
import { apolloClient } from "@/apollo-config";
import {
    updateMinMaxAmountCoins,
    fetchCoinsForAmount,
    fetchAmountForCoins,
} from './utils';
import animHandshake from '@/assets/lottie/handshake.json';
import { useUserStore } from "@/stores/user";


// <<<STORES>>>
const userStore = useUserStore();
const currenciesStore = useCurrenciesStore();
const currencies = computed(() => currenciesStore.currencies);
const coinsStore = useCoinsStore();
const coins = computed(() => coinsStore.coins);


// <<<STATES>>>
const selectedCode = ref(null);             // Локальное состояние для выбранного кода валют
const selectedTicker = ref(null);           // Локальное состояние для выбранного тикета
const amountCurrency = ref('');             // Локальное состояние для суммы
const isValidCurrency = ref(true);          // Состояние для валидации
const minAmountCoins = ref(null);
const maxAmountCoins = ref(null);
const amountCoins= ref('');                 // Локальное состояние для количества монет
const isValidCoins = ref(true);             // Состояние для валидации
const selectedPaymentMethod = ref(null);
const isSubmitted = ref(false);
const isActivePayButton = ref(false);
const formVisible = ref(true);              // Форма видна
const animationVisible = ref(false);        // Анимация видна


// <<<COMPUTED>>>
const selectedCurrency = computed(() => {
    return currencies.value.find((currency) => currency.code === selectedCode.value);   // Находим валюту по коду
});

// Вычисляем минимальную и максимальную сумму на основе выбранной валюты
const minAmountCurrency = computed(() => {
    const value = selectedCurrency.value?.minAmount || 0;
    return parseFloat(value); // Преобразуем в число
});

const maxAmountCurrency = computed(() => {
    const value = selectedCurrency.value?.maxAmount || Infinity;
    return parseFloat(value); // Преобразуем в число
});

const selectedCoin = computed(() => {
    return coins.value.find((coin) => coin.ticker === selectedTicker.value);   // Находим монету по тикету
});

const selectedMethod = computed(() =>
    selectedCurrency.value.paymentMethods.find(method => method.id === selectedPaymentMethod.value)
);


// <<<watch && WatchEffect>>>

// Реакция на изменение списка валют
watchEffect(() => {
    if (currencies.value.length > 0 && !selectedCode.value) {
        selectedCode.value = currencies.value[0].code; // Инициализируем код первой валюты
    }
});

// Реакция на изменение списка монет
watchEffect(() => {
    if (coins.value.length > 0 && !selectedTicker.value) {
        selectedTicker.value = coins.value[0].ticker; // Инициализируем тикер первой монеты
    }
});

// Очистка полей при смене валюты
watch([selectedCode, selectedTicker], () => {
    amountCurrency.value = ""; // Очищаем поле суммы
    amountCoins.value = ""; // Очищаем поле количества монет
    // Сбрасываем состояние валидации
    isValidCurrency.value = true;
    isValidCoins.value = true;
});

watchEffect(async () => {
    if (
        (minAmountCurrency.value !== null && minAmountCurrency.value !== undefined) ||
        (maxAmountCurrency.value !== null && maxAmountCurrency.value !== undefined)
    ) {
        const formData = {
            selectedCurrency: selectedCurrency,
            selectedTicker: selectedTicker,
            minAmountCurrency: minAmountCurrency,
            minAmountCoins: minAmountCoins,
            maxAmountCurrency: maxAmountCurrency,
            maxAmountCoins: maxAmountCoins,
        };

        await updateMinMaxAmountCoins(formData);
    }
});


// <<<VALIDATION>>>

// Функция для валидации суммы
const validateCurrencyInput = debounce(async (event) => {
    let value = event.target.value;

    // Оставляем только цифры, точку и запятую
    value = value.replace(/[^\d.,]/g, '');

    // Заменяем запятую на точку, если точка еще нет
    if (!value.includes('.')) {
        value = value.replace(',', '.');
    } else {
        // Если точка уже есть, удаляем запятую
        value = value.replace(',', '');
    }

    // Убираем все дополнительные точки, оставляем только первую
    const parts = value.split('.');
    if (parts.length > 1) {
        value = parts[0] + '.' + parts[1].slice(0, 2); // Ограничиваем 2 знаками после точки
    } else {
        value = parts[0];
    }

    // Обновляем значение
    amountCurrency.value = value;

    // Проверка на минимальное и максимальное значение
    const numericValue = parseFloat(amountCurrency.value || 0); // Преобразуем строку в число

    // Проверка на пустое поле и отправка запроса
    if (amountCurrency.value === '' || amountCurrency.value === '.') {
        isValidCurrency.value = true; // Если поле пустое, ошибка не показывается
        amountCoins.value = '';
    } else if (numericValue < minAmountCurrency.value || numericValue > maxAmountCurrency.value) {
        isValidCurrency.value = false; // Если значение не соответствует ограничениям, показываем ошибку
        amountCoins.value = '';
    } else {
        isValidCurrency.value = true; // Если значение корректное, ошибка исчезает

        const formData = {
            amount: numericValue,
            currencyCode: selectedCurrency.value.code,
            coinTicker: selectedTicker.value,
        };

        amountCoins.value = await fetchCoinsForAmount(formData);
    }

}, 500); // Задержка 500 мс


const validateCoinsInput = debounce(async (event) => {
    let value = event.target.value;

    // Оставляем только цифры, точку и запятую
    value = value.replace(/[^\d.,]/g, '');

    // Заменяем запятую на точку, если точка еще нет
    if (!value.includes('.')) {
        value = value.replace(',', '.');
    } else {
        // Если точка уже есть, удаляем запятую
        value = value.replace(',', '');
    }

    // Убираем все дополнительные точки, оставляем только первую
    const parts = value.split('.');
    if (parts.length > 1) {
        value = parts[0] + '.' + parts[1].slice(0, 8); // Ограничиваем 8 знаками после точки
    } else {
        value = parts[0];
    }

    // Обновляем значение
    amountCoins.value = value;

    // Проверка на минимальное и максимальное значение
    const numericValue = parseFloat(amountCoins.value || 0); // Преобразуем строку в число

    // Проверка на пустое поле и отправка запроса
    if (amountCoins.value === '' || amountCoins.value === '.') {
        isValidCoins.value = true; // Если поле пустое, ошибка не показывается
        amountCurrency.value = '';
    } else if (numericValue < minAmountCoins.value || numericValue > maxAmountCoins.value) {
        isValidCoins.value = false; // Если значение не соответствует ограничениям, показываем ошибку
        amountCurrency.value = '';
    } else {
        isValidCoins.value = true; // Если значение корректное, ошибка исчезает

        const formData = {
            amount: numericValue,
            currencyCode: selectedCurrency.value.code,
            coinTicker: selectedTicker.value,
        };

        amountCurrency.value = await fetchAmountForCoins(formData);
    }
}, 500);


const validateForm = () => {
    // Проверяем валидность суммы валюты
    if (!isValidCurrency.value || !amountCurrency.value) {
        return false;
    }

    // Проверяем валидность суммы монет
    if (!isValidCoins.value || !amountCoins.value) {
        return false;
    }

    // Проверяем, выбрана ли платежная система
    if (!selectedPaymentMethod.value) {
        return false;
    }

    // Если все проверки пройдены
    return true;
};

// Функция для очистки полей формы
const resetForm = () => {
    amountCurrency.value = '';
    amountCoins.value = '';
    selectedPaymentMethod.value = null;
    isValidCurrency.value = true;
    isValidCoins.value = true;
    isSubmitted.value = false;
};


// Функция завершения анимации
const onAnimationFinish = () => {
    resetForm();  // сбрасываем форму форму

    // После окончания анимации показываем форму снова
    formVisible.value = true;
    animationVisible.value = false;
};


const handleSubmit = async () => {
    isActivePayButton.value = true;
    isSubmitted.value = true;

    // Убираем активный класс через 300ms (время длительности анимации)
    setTimeout(() => {
        isActivePayButton.value = false;
    }, 300);

    // Вызываем функцию валидации
    if (validateForm()) {
        const formData = {
            coinName: selectedCoin.value?.name,
            coinTicker: selectedTicker.value,
            coinAmount: parseFloat(amountCoins.value).toFixed(8),
            currency: selectedCurrency.value?.name,
            currencyCode: selectedCode.value,
            totalPrice: amountCurrency.value.toString(),
            paymentMethod: selectedMethod.value?.name,
        };

        const order = await userStore.createOrder(formData);

        if (order) {
            const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
            await sleep(500);

            // Скрываем форму и показываем анимацию
            formVisible.value = false;
            animationVisible.value = true;
        }

    } else {
        console.error("Форма не валидирована");
    }
};

</script>

<style lang="scss" scoped>
@use "./style.scss";
</style>