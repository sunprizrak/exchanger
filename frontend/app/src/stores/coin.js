import { defineStore } from "pinia";
import { apolloClient } from "@/apollo-config";
import { GET_ALL_COINS } from "@/queries"

export const useCoinsStore = defineStore({
    id: "coins",
    state: () => ({
        coins: [],
    }),
    actions: {
        async loadCoins() {
            if (this.coins.length === 0) {
                try {
                    // Выполняет GraphQl-запрос
                    const { data } = await apolloClient.query({
                        query: GET_ALL_COINS,
                    });
                    // Сохраняет полученные данные в state
                    this.coins = data.allCoins;
                    console.log(this.coins);
                } catch (error) {
                    console.error("Error loading coins:", error);
                }
            }
        },
    },
});