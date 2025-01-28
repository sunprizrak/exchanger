import { defineStore } from "pinia";
import { GET_ALL_ORDERS, GET_ORDER_STATUS } from "@/queries";
import { apolloClient } from "@/apollo-config";
import { CREATE_ORDER } from "@/mutations";

export const useUserStore = defineStore({
    id: "user",
    state: () => ({
        token: localStorage.getItem("token") || null,
        user: JSON.parse(localStorage.getItem("user")) || null,
        orders: [],
        orderStatusPollingInterval: null,
    }),
    getters: {
        getToken: (state) => state.token,
        getUser: (state) => state.user,
        getOrders: (state) => state.orders,
    },
    actions: {
        setToken(token) {
            this.token = token;

            // Save token to local storage
            localStorage.setItem("token", this.token);
        },
        removeToken() {
            this.token = null;

            // Delete token from local storage
            localStorage.removeItem("token");
        },
        setUser(user) {
            this.user = JSON.stringify(user);

            // Save user to local storage
            localStorage.setItem("user", this.user);
        },
        removeUser() {
            this.user = null;

            // Delete user from local storage
            localStorage.removeItem("user");
        },

        // Функция для создания ордера
        async createOrder(formData) {
            try {
                // Вызов мутации через Apollo
                const { data } = await apolloClient.mutate({
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

                return true;
            } catch (error) {
                alert("Что-то пошло не так. Мы уже работаем над этим.", error.message);
            }
        },

        async loadOrders() {
            try {
                // Выполняет GraphQl-запрос
                const { data } = await apolloClient.query({
                    query: GET_ALL_ORDERS,
                    fetchPolicy: 'no-cache', // Отключает кеширование
                });

                this.orders = data.allOrders;
            } catch (error) {
                alert("Error loading orders:", error.message);
            }
        },

        // Добавление нового ордера в хранилище
        setOrder(newOrder) {
            this.orders.unshift(newOrder); // Добавляем новый ордер в начало списка
        },

        // Функция для обновления статусов ордеров
        async updateOrderStatuses() {
            try {
                for (let order of this.orders) {
                    // Пропускаем ордера с статусами CANCELLED или COMPLETED
                    if (order.status === 'CANCELLED' || order.status === 'COMPLETED') {
                        continue;
                    }

                    const { data } = await apolloClient.query({
                        query: GET_ORDER_STATUS,
                        variables: {
                            orderId: order.id
                        },
                        fetchPolicy: 'no-cache', // Отключает кеширование
                    });

                    const updatedStatus = data.orderStatus;
                    console.log(updatedStatus);
                    // Если статус ордера изменился, обновляем его в списке
                    if (updatedStatus !== order.status) {
                    // Находим ордер в списке и создаем новый объект с обновленным статусом
                    const orderIndex = this.orders.findIndex(o => o.id === order.id);
                    if (orderIndex !== -1) {
                        // Создаем новый объект ордера с обновленным статусом
                        this.orders[orderIndex] = {
                            ...this.orders[orderIndex],
                            status: updatedStatus
                        };
                    }
                }
                }
            } catch (error) {
                console.error("Error updating order statuses:", error.message);
            }
        },

        // Функция для запуска polling каждые x секунд
        startOrderStatusPolling() {
            // Останавливаем предыдущие интервалы, если они были
            if (this.orderStatusPollingInterval) {
                clearInterval(this.orderStatusPollingInterval);
            }

            // Устанавливаем новый интервал для запроса статусов каждые x секунд
            this.statusPollingInterval = setInterval(async () => {
                await this.updateOrderStatuses();
            }, 30000); // 30 секунд
        },

        // Функция для остановки polling
        stopOrderStatusPolling() {
            if (this.orderStatusPollingInterval) {
                clearInterval(this.orderStatusPollingInterval);
                this.orderStatusPollingInterval = null;
            }
        }
    },
});