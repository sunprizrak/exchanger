import { apolloClient } from "@/apollo-config";
import { GET_COINS_FOR_AMOUNT, GET_AMOUNT_FOR_COINS } from "@/queries";


// Функция для получения количества монет по сумме
export const fetchCoinsForAmount = async (amount, currencyCode, coinTicker) => {
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
export const fetchAmountForCoins = async (amount, currencyCode, coinTicker) => {
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


export const updateMinMaxAmountCoins = async (
    selectedCurrency,
    selectedTicker,
    minAmountCurrency,
    minAmountCoins,
    maxAmountCurrency,
    maxAmountCoins,
) => {
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