
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
                    <input
                        type="text"
                        v-model="amount"
                        @input="validateAmount"
                        placeholder="Введите сумму"
                        required
                    />
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
                    <input type="number" placeholder="колличество"/>
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
import { computed, ref, watchEffect } from "vue";

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

// Находим монету по тикеру
const selectedCoin = computed(() => {
    return coins.value.find((coin) => coin.ticker === selectedTicker.value);
});

const amount = ref('');  // Локальное состояние для суммы

// Функция для валидации ввода
const validateAmount = (event) => {
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
};

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