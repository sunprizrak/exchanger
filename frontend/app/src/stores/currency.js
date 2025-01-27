import { defineStore } from 'pinia';
import { apolloClient } from '@/apollo-config';
import { GET_ALL_CURRENCIES } from "@/queries";


export const useCurrenciesStore = defineStore({
    id: "currencies",
    state: () => ({
        currencies: [],
    }),
    actions: {
        async loadCurrencies() {
            if (this.currencies.length === 0) {
                try {
                    const { data } = await apolloClient.query({
                        query: GET_ALL_CURRENCIES,
                    });

                    // Сохраняем данные в состоянии
                    this.currencies = data.allCurrencies;
                } catch (error) {
                    alert('Error loading currency:', error.message);
                }
            }
        },
    },
});