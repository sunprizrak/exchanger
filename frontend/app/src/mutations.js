import gql from "graphql-tag";

export const USER_SIGNUP = gql`
    mutation ($tgId: String!, $tgUsername: String!) {
        createUser(tgId: $tgId, tgUsername: $tgUsername) {
            // request from server
            user {
                tgId
                tgUsername
            }
        }
    }
`;