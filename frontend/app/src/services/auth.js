import { apolloClient } from "@/apollo-config";
import { TG_AUTH } from "@/mutations";
import { useUserStore } from "@/stores/user";


export async function telegramAuth(initData) {
    try {
        // Вызов мутации через Apollo
        const response = await apolloClient.mutate({
            mutation: TG_AUTH,
            variables: {
                initData: initData,
            },
        });

        // Извлекаем данные из ответа
        const { token, user } = response.data.telegramAuth;

        const userStore = useUserStore();
        userStore.setToken(token);
        userStore.setUser(user);
    } catch (error) {
        // alert("Что-то пошло не так. Мы уже работаем над этим.");
        alert(error);
    }
};


