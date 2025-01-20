
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
                            v-model="amount"
                            @input="validateAmount"
                            :min="minAmount"
                            :max="maxAmount"
                            placeholder="Введите сумму"
                            required
                        />
                        <p class="error" v-if="!isValid">
                            <span v-if="amount < minAmount">min: {{ selectedCurrency.symbol }}{{ minAmount.toFixed(2) }}</span>
                            <span v-else-if="amount > maxAmount">max: {{ selectedCurrency.symbol }}{{ maxAmount.toFixed(2) }}</span>
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
                            type="number"
                            placeholder="колличество"
                            :value="coinsAmount"
                        />
                    </div>
                </div>
            </div>
        </form>
        <div class="form-button">
            <div>купить</div>
        </div>
    </div>
</template>


<script setup>
import { useCoinsStore } from "@/stores/coin";
import { useCurrenciesStore } from "@/stores/currency";
import { computed, ref, watchEffect, watch } from "vue";
import debounce from 'lodash.debounce';
import { apolloClient } from "@/apollo-config";
import { GET_COINS_FOR_AMOUNT } from "@/queries";


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
const minAmount = computed(() => {
    const value = selectedCurrency.value?.minAmount || 0;
    return parseFloat(value); // Преобразуем в число
});

const maxAmount = computed(() => {
    const value = selectedCurrency.value?.maxAmount || Infinity;
    return parseFloat(value); // Преобразуем в число
});

const amount = ref('');  // Локальное состояние для суммы
const isValid = ref(true);  // Состояние для валидации

// Функция для валидации ввода
const validateAmount = debounce(async (event) => {
    let value = event.target.value;

    // Оставляем только цифры и точку
    value = value.replace(/[^\d.]/g, '');

    // Ограничиваем количество знаков после точки до 2
    const parts = value.split('.');
    if (parts.length > 1) {
        // Оставляем только первые два знака после точки
        parts[1] = parts[1].slice(0, 2);
        value = parts.join('.');
    }

    // Обновляем значение
    amount.value = value;

    // Проверка на минимальное и максимальное значение
    const numericValue = parseFloat(amount.value || 0); // Преобразуем строку в число

    // Проверка на пустое поле и отправка запроса
    if (amount.value === '') {
        isValid.value = true; // Если поле пустое, ошибка не показывается
    } else if (numericValue < minAmount.value || numericValue > maxAmount.value) {
        isValid.value = false; // Если значение не соответствует ограничениям, показываем ошибку
    } else {
        isValid.value = true; // Если значение корректное, ошибка исчезает
        await fetchCoinsForAmount(numericValue);
    }

}, 500); // Задержка 500 мс

const coinsAmount = ref(null);

// Функция для отправки GraphQL запроса количества монет
const fetchCoinsForAmount = async (amount) => {
    try {
        const response = await apolloClient.query({
            query: GET_COINS_FOR_AMOUNT,
            variables: {
                amount: amount,
                currencyCode: selectedCurrency.value.code,
                coinTicker: selectedTicker.value,
            },
        });
        coinsAmount.value = response.data.coinsAmount; // Результат запроса
    } catch (error) {
        console.error("Ошибка при получении данных", error);
    }
};

// Очистка полей при смене валюты или монеты
watch([selectedCode, selectedTicker], () => {
    amount.value = ""; // Очищаем поле суммы
    coinsAmount.value = null; // Очищаем результат запроса
    isValid.value = true; // Сбрасываем состояние валидации
});

</script>

<style lang="scss" scoped>
.form-wrap {
    display: flex;
    flex-direction: column;
    width: 80%;
    height: auto;
    position: absolute;
    border-radius: 7px;

    border: 4px solid var(--color-border);

    form {
        display: flex;
        flex-direction: column;
        padding: 10px;

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