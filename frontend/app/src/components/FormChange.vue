
<template>
    <div class="form-wrap">
        <form>
            <div class="group-input">
                <span>Вы отправляете</span>
                <div class="bottom-line">
                    <div class="country">
                        <img src="#"/>
                        <select>
                            <option>RUB</option>
                            <option>BYN</option>
                        </select>
                    </div>
                    <input type="number" placeholder="сумма"/>
                </div>
            </div>
            <hr/>
            <div class="group-input">
                <span>Вы получаете</span>
                <div class="bottom-line">
                    <div class="coins">
                        <img v-if="selectedCoin" :src="selectedCoin.fullIconUrl" alt="Coin Icon" />
                        <select v-model="selectedTicker">
                            <option
                                v-for="coin in coins"
                                :key="coin.ticker"
                                :value="coin.ticker"
                            >
                                {{ coin.ticker }}
                            </option>
                        </select>
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
import { computed, ref, watchEffect } from "vue";

const coinsStore = useCoinsStore();
const coins = computed(() => coinsStore.coins);

// Локальное состояние для выбранного тикера
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
                    width: auto;

                    img {
                        height: 25px;
                        width: 25px;
                        border-radius: 50%;
                        flex-shrink: 0;
                    }

                    select {
                        background-color: transparent;
                        background-position: right 0.2rem center;
                        border: 0;
                        outline: none;
                        box-shadow: none;
                        font-weight: bold;
                        padding-right: 0;
                        min-width: 65px;
                        width: auto;
                    }

                }

                input {
                    flex-grow: 1;
                    background-color: transparent;
                    border: 0;
                    outline: none;
                    box-shadow: none;
                    text-align: right;
                    width: auto;
                    min-width: 150px;
                    padding: 0;
                    caret-color: var(--color-text);
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