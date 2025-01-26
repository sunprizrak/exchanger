import { GET_ALL_ORDERS } from "@/queries";
import { apolloClient } from "@/apollo-config";


// Функция для получения ордеров
export async function getAllOrders() {
    try {
        // Вызов мутации через Apollo
        const { data } = await apolloClient.query({
            query: GET_ALL_ORDERS,
        });

        // Извлекаем данные из ответа
        const orders = data.allOrders;
        return orders
    } catch (error) {
        alert("Что-то пошло не так. Мы уже работаем над этим.");
    }
};