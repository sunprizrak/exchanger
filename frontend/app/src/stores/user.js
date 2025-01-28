import { defineStore } from "pinia";
import { GET_ALL_ORDERS } from "@/queries";
import { apolloClient } from "@/apollo-config";
import { CREATE_ORDER, GET_ORDER_STATUS } from "@/mutations";

export const useUserStore = defineStore({
    id: "user",
    state: () => ({
        token: localStorage.getItem("token") || null,
        user: JSON.parse(localStorage.getItem("user")) || null,
        orders: [],
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

                // Добавляем новый ордер в ордера
                const newOrder = data.createOrder.order;
                this.setOrder(newOrder);
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
                });

                data.allOrders.forEach(newOrder => {
                    const exists = this.orders.some(order => String(order.id) === String(newOrder.id));
                    if (!exists) {
                        this.setOrder(newOrder); // Добавляем только новые ордера
                    }
                });
            } catch (error) {
                alert("Error loading orders:", error.message);
            }
        },

        // Добавление нового ордера в хранилище
        setOrder(newOrder) {
            this.orders.unshift(newOrder); // Добавляем новый ордер в начало списка
        }

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
                        variables: { orderId: order.id },
                    });

                    const updatedOrder = data.order;
                    if (updatedOrder.status !== order.status) {
                        // Обновляем статус ордера в списке
                        const orderIndex = this.orders.findIndex(o => o.id === updatedOrder.id);
                        if (orderIndex !== -1) {
                            this.orders[orderIndex] = updatedOrder;
                        }
                    }
                }
            } catch (error) {
                console.error("Error updating order statuses:", error.message);
            }
        },

        // Функция для запуска polling каждые 30 секунд
        startStatusPolling() {
            // Останавливаем предыдущие интервалы, если они были
            if (this.statusPollingInterval) {
                clearInterval(this.statusPollingInterval);
            }

            // Устанавливаем новый интервал для запроса статусов каждые 30 секунд
            this.statusPollingInterval = setInterval(async () => {
                await this.updateOrderStatuses();
            }, 30000); // 30 секунд
        },

        // Функция для остановки polling
        stopStatusPolling() {
            if (this.statusPollingInterval) {
                clearInterval(this.statusPollingInterval);
                this.statusPollingInterval = null;
            }
        }
    },
});