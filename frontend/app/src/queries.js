import gql from "graphql-tag"

export const USER_INFO = gql`
    query {
        user {
            email
        }
    }
`;

export const GET_ALL_COINS = gql`
    query {
        allCoins {
            name
            ticker
            fullIconUrl
            priceUsd
            priceRub
            commissionRate
        }
    }
`;
