import { apolloClient } from "@/apollo-config";
import { GET_COINS_FOR_AMOUNT, GET_AMOUNT_FOR_COINS } from "@/queries";
import { CREATE_ORDER } from "@/mutations";


// Функция для создания ордера
export async function submitPaymentForm(formData) {
    try {
        // Вызов мутации через Apollo
        const response = await apolloClient.mutate({
            mutation: CREATE_ORDER,
            variables: {
                coinName: formData.coinName,
                coinTicker: formData.coinTicker,
                coinAmount: formData.coinAmount,
                currency: formData.currency,
                currencyCode: formData.currencyCode,
                totalPrice: formData.totalPrice,
                paymentMethod: formData.paymentMethod,
            },
        });

        // Извлекаем данные из ответа
        const message = response.data.createOrder.message;
        console.log(message);  // Выводим сообщение от сервера
    } catch (error) {
        // alert("Что-то пошло не так. Мы уже работаем над этим.");
        console.log('error', error);
    }
};

// Функция для получения количества монет по сумме
export const fetchCoinsForAmount = async (formData) => {
    try {
        const response = await apolloClient.query({
            query: GET_COINS_FOR_AMOUNT,
            variables: {
                amount: formData.amount,
                currencyCode: formData.currencyCode,
                coinTicker: formData.coinTicker,
            },
        });
        return response.data.coinsAmount; // Результат запроса
    } catch (error) {
        alert("Что-то пошло не так. Мы уже работаем над этим.");
    }
};

// Запрос для получения суммы по количеству монет
export const fetchAmountForCoins = async (formData) => {
    try {
        const response = await apolloClient.query({
            query: GET_AMOUNT_FOR_COINS,
            variables: {
                amount: formData.amount,
                currencyCode: formData.currencyCode,
                coinTicker: formData.coinTicker,
            },
        });
        return response.data.currencyAmount; // Результат запроса
    } catch (error) {
        alert("Что-то пошло не так. Мы уже работаем над этим.");
    }
};


export const updateMinMaxAmountCoins = async (formData) => {
    const { selectedCurrency, selectedTicker, minAmountCurrency, minAmountCoins, maxAmountCurrency, maxAmountCoins } = formData;

    try {
        if (!selectedCurrency.value || !selectedCurrency.value.code) {
            return;
        }

        // Условие, чтобы запрос не выполнялся при загрузке, если minAmountCurrency не задано (null, undefined или пустая строка)
        if (minAmountCurrency.value != null) {
            const formDataMin = {
                amount: minAmountCurrency.value,
                currencyCode: selectedCurrency.value.code,
                coinTicker: selectedTicker.value,
            };
            const valueMin = await fetchCoinsForAmount(formDataMin);
            minAmountCoins.value = parseFloat(valueMin) || 0; // Преобразуем в число, подстраховываемся от undefined
        }

        // Условие, чтобы запрос не выполнялся при загрузке, если maxAmountCurrency не задано (null, undefined или пустая строка)
        if (maxAmountCurrency.value != null) {
            const formDataMax = {
                amount: maxAmountCurrency.value,
                currencyCode: selectedCurrency.value.code,
                coinTicker: selectedTicker.value,
            };
            const valueMax = await fetchCoinsForAmount(formDataMax);
            maxAmountCoins.value = parseFloat(valueMax) || Infinity;
        }
    } catch (error) {
        alert("Что-то пошло не так. Мы уже работаем над этим.");
    }
};