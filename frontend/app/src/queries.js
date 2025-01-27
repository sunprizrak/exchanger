import gql from "graphql-tag"


export const GET_ALL_COINS = gql`
    query {
        allCoins {
            name
            ticker
            fullIconUrl
            priceUsd
            priceRub
        }
    }
`;

export const GET_ALL_CURRENCIES = gql`
    query {
        allCurrencies {
            id
            name
            code
            symbol
            fullIconUrl
            minAmount
            maxAmount
            paymentMethods {
                id
                name
                fullIconUrl
            }
        }
    },
`;

export const GET_COINS_FOR_AMOUNT = gql`
    query ($amount: Float!, $currencyCode: String!, $coinTicker: String!) {
        coinsAmount(amount: $amount, currencyCode: $currencyCode, coinTicker: $coinTicker)
    },
`;

export const GET_AMOUNT_FOR_COINS = gql`
    query ($amount: Float!, $currencyCode: String!, $coinTicker: String!) {
        currencyAmount(amount: $amount, currencyCode: $currencyCode, coinTicker: $coinTicker)
    },
`;

export const GET_ALL_ORDERS = gql`
    query {
        allOrders {
            id
            coinName
            coinTicker
            coinAmount
            currency
            currencyCode
            paymentMethod
            totalPrice
            status
            createdFormatted
        }
    }
`;