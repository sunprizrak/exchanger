import gql from "graphql-tag"

export const USER_INFO = gql`
    query {
        user {
            email
        }
    }
`;
