<template>
    <div class="form-wrap">
        <form>
            <div class="group-input">
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
                    </div>
                </div>
            </div>
            <hr/>
            <div class="group-input">
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
                    </div>
                </div>
            </div>
            <hr/>
            <div>
                <span>Методы оплаты:</span>
                <ul v-if="selectedCurrency.paymentMethods && selectedCurrency.paymentMethods.length > 0">
                    <li v-for="method in selectedCurrency.paymentMethods" :key="method.id">{{ method.name }}</li>
                </ul>
                <p v-else>Нет доступных методов оплаты</p>
            </div>
        </form>
        <div class="form-button" @click="handleSubmit">
            <div>КУПИТЬ</div>
        </div>
    </div>
</template>


<script setup>
import { useCoinsStore } from "@/stores/coin";
import { useCurrenciesStore } from "@/stores/currency";
import { computed, ref, watchEffect, watch } from "vue";
import debounce from 'lodash.debounce';
import { apolloClient } from "@/apollo-config";
import { GET_COINS_FOR_AMOUNT, GET_AMOUNT_FOR_COINS } from "@/queries";

// Функция для получения количества монет по сумме
const fetchCoinsForAmount = async (amount, currencyCode, coinTicker) => {
    try {
        const response = await apolloClient.query({
            query: GET_COINS_FOR_AMOUNT,
            variables: {
                amount: amount,
                currencyCode: currencyCode,
                coinTicker: coinTicker,
            },
        });
        return response.data.coinsAmount; // Результат запроса
    } catch (error) {
        console.error("Ошибка при получении данных", error);
    }
};

// Запрос для получения суммы по количеству монет
const fetchAmountForCoins = async (amount, currencyCode, coinTicker) => {
    try {
        const response = await apolloClient.query({
            query: GET_AMOUNT_FOR_COINS,
            variables: {
                amount: amount,
                currencyCode: currencyCode,
                coinTicker: coinTicker,
            },
        });
        return response.data.currencyAmount; // Результат запроса
    } catch (error) {
        console.error("Ошибка при получении суммы", error);
    }
};


const currenciesStore = useCurrenciesStore();
const currencies = computed(() => currenciesStore.currencies);

// Локальное состояние для выбранного кода валют
const selectedCode = ref(null);

// Реакция на изменение списка валют
watchEffect(() => {
    if (currencies.value.length > 0 && !selectedCode.value) {
        selectedCode.value = currencies.value[0].code; // Инициализируем код первой валюты
    }
});

// Находим валюту по коду
const selectedCurrency = computed(() => {
    return currencies.value.find((currency) => currency.code === selectedCode.value);
});

const coinsStore = useCoinsStore();
const coins = computed(() => coinsStore.coins);

// Локальное состояние для выбранного тикета
const selectedTicker = ref(null);

// Реакция на изменение списка монет
watchEffect(() => {
    if (coins.value.length > 0 && !selectedTicker.value) {
        selectedTicker.value = coins.value[0].ticker; // Инициализируем тикер первой монеты
    }
});

// Находим монету по тикету
const selectedCoin = computed(() => {
    return coins.value.find((coin) => coin.ticker === selectedTicker.value);
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

const amountCurrency = ref('');  // Локальное состояние для суммы
const isValidCurrency = ref(true);  // Состояние для валидации

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
    if (amountCurrency.value === '') {
        isValidCurrency.value = true; // Если поле пустое, ошибка не показывается
        amountCoins.value = '';
    } else if (numericValue < minAmountCurrency.value || numericValue > maxAmountCurrency.value) {
        isValidCurrency.value = false; // Если значение не соответствует ограничениям, показываем ошибку
        amountCoins.value = '';
    } else {
        isValidCurrency.value = true; // Если значение корректное, ошибка исчезает
        amountCoins.value = await fetchCoinsForAmount(numericValue, selectedCurrency.value.code, selectedTicker.value);
    }

}, 500); // Задержка 500 мс


// Вычисляем минимальную и максимальную сумму монеты на основе валюты
const minAmountCoins = ref(null);
const maxAmountCoins = ref(null);

const updateMinMaxAmountCoins = async () => {
    try {
        if (!selectedCurrency.value || !selectedCurrency.value.code) {
            return;
        }

        if (minAmountCurrency.value) {
            const valueMin = await fetchCoinsForAmount(minAmountCurrency.value, selectedCurrency.value.code, selectedTicker.value);
            minAmountCoins.value = parseFloat(valueMin) || 0; // Преобразуем в число, подстраховываемся от undefined
        }

        if (maxAmountCurrency.value) {
            const valueMax = await fetchCoinsForAmount(maxAmountCurrency.value, selectedCurrency.value.code, selectedTicker.value);
            maxAmountCoins.value = parseFloat(valueMax) || Infinity; // Преобразуем в число, подстраховываемся от undefined
        }
    } catch (error) {
        console.error("Ошибка при получении данных в updateMinMaxAmountCoins", error);
    }
};

watchEffect(() => {
    if (
        (minAmountCurrency.value !== null && minAmountCurrency.value !== undefined) ||
        (maxAmountCurrency.value !== null && maxAmountCurrency.value !== undefined)
    ) {
        updateMinMaxAmountCoins();
    }
});


const amountCoins= ref(''); // Локальное состояние для количества монет
const isValidCoins = ref(true);  // Состояние для валидации

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
    if (amountCoins.value === '') {
        isValidCoins.value = true; // Если поле пустое, ошибка не показывается
        amountCurrency.value = '';
    } else if (numericValue < minAmountCoins.value || numericValue > maxAmountCoins.value) {
        isValidCoins.value = false; // Если значение не соответствует ограничениям, показываем ошибку
        amountCurrency.value = '';
    } else {
        isValidCoins.value = true; // Если значение корректное, ошибка исчезает
        amountCurrency.value = await fetchAmountForCoins(numericValue, selectedCurrency.value.code, selectedTicker.value);
    }
}, 500);

// Очистка полей при смене валюты или монеты
watch([selectedCode, selectedTicker], () => {
    amountCurrency.value = ""; // Очищаем поле суммы
    amountCoins.value = ""; // Очищаем поле количества монет
    // Сбрасываем состояние валидации
    isValidCurrency.value = true;
    isValidCoins.value = true;
});

const handleSubmit = () => {
    // Проверка валидности значений
    //if (isValidCurrency.value && isValidCoins.value && amountCurrency.value && amountCoins.value) {
    //    isFlipped.value = !isFlipped.value; // Разворачиваем/сворачиваем форму
    //}
    isFlipped.value = !isFlipped.value; // Разворачиваем/сворачиваем форму
};

</script>

<style lang="scss" scoped>

.form-wrap {
    display: flex;
    flex-direction: column;
    width: 80%;
    height: auto;
    border-radius: 7px;
    border: 4px solid var(--color-border);

    form {
        display: flex;
        flex-direction: column;
        padding: 10px;
        position: relative;

        .group-input {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 100%;

            span {
                display: inline-block;
                white-space: nowrap;
                font-weight: bold;
                font-size: 12px;
            }

            .bottom-line {
                display: flex;
                flex-direction: row;
                width: 100%;

                .country, .coins {
                    display: flex;
                    flex-direction: row;
                    align-items: center;
                    width: fit-content;

                    img {
                        height: 35px;
                        width: 35px;
                        border-radius: 50%;
                    }

                    div {
                        width: fit-content;


                        select {
                            background-color: transparent;
                            border: 0;
                            outline: none;
                            box-shadow: none;
                            font-weight: bold;
                        }

                        span {
                            display: inline-block;
                            white-space: nowrap;
                            font-weight: bold;
                            font-size: 12px;
                            padding-left: 0.75rem;
                        }
                    }
                }

                .box-input {
                    position: relative;
                    height: auto;

                    input {
                        background-color: transparent;
                        box-sizing: border-box;
                        border: 0;
                        outline: none;
                        box-shadow: none;
                        text-align: right;
                        padding: 0;
                        caret-color: var(--color-text);
                        width: 100%;
                        height: 100%;
                    }

                    p {
                        position: absolute;
                        right: 0;
                        bottom: 0;
                    }
                }
            }
        }
    }

    .form-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 50px;
        width: 100%;
        background-color: #000;
        padding-top: 4px;

        div {
            cursor: pointer;
            background-color: var(--color-background);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 1px;
            transition: 0.2s;
            box-shadow: inset 0 20px 4px -21px rgba(255,255,255,0.4), 0 19px 13px 0 rgba(0,0,0,0.3);
            position: relative;
            z-index: 2;
            border-bottom-left-radius: 5px;
            border-bottom-right-radius: 5px;
            font-weight: bold;
            user-select: none;

            &:active {
                background-image: linear-gradient(to top, #151515 0%, #1d1d1d 100%);
                box-shadow: inset 0 16px 14px -21px transparent, 0 0px 13px 0 rgba(0,0,0,0.3), inset 0 0 7px 2px rgba(0,0,0,0.4);
                z-index: 0;
            }
        }
    }
}

</style>