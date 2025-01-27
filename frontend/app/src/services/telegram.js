import { apolloClient } from "@/apollo-config";
import { TG_AUTH } from "@/mutations";


// Проверяем, является ли приложение WebApp в Telegram
export const telegram = {
    get isWebApp() {
        return window.Telegram && window.Telegram.WebApp ? true : false;
    }
};

// Инициализация Web App
export async function initializeTelegram() {
    try {
        // Уведомляем Telegram о готовности приложения
        window.Telegram.WebApp.ready();

        // Получение данных initData
        const telegramData = window.Telegram.WebApp.initData;
        if (!telegramData) {
            throw new Error("initData пустой. Убедитесь, что Telegram WebApp передает корректные данные.");
        }
        return telegramData;
    } catch (error) {
        throw error; // Прокидываем ошибку дальше для обработки в вызывающем коде
    }
}


export async function telegramAuth(initData) {
    try {
        // Вызов мутации через Apollo
        const { data } = await apolloClient.mutate({
            mutation: TG_AUTH,
            variables: {
                initData: initData,
            },
        });

        return { token: data.telegramAuth.token, user: data.telegramAuth.user };
    } catch (error) {
        alert("Error auth, Что-то пошло не так. Мы уже работаем над этим.", error.message);
    }
};