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