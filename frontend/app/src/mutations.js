import gql from "graphql-tag";


export const TG_AUTH = gql`
    mutation ($initData: String!) {
        telegramAuth(initData: $initData) {
            token
            user {
                tgId
                tgUsername
            }
        }
    }
`;


export const CREATE_ORDER = gql`
    mutation (
        $coinName: String!,
        $coinTicker: String!,
        $coinAmount: String!,
        $currency: String!,
        $currencyCode: String!,
        $totalPrice: String!,
        $paymentMethod: String!
    ) {
        createOrder(
            coinName: $coinName,
            coinTicker: $coinTicker,
            coinAmount: $coinAmount,
            currency: $currency,
            currencyCode: $currencyCode,
            totalPrice: $totalPrice,
            paymentMethod: $paymentMethod
        ) {
            message
        }
    }
`;