export const telegramUtils = {
    get isTelegramWebApp() {
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
        console.error("Ошибка в initializeTelegram:", error.message);
        throw error; // Прокидываем ошибку дальше для обработки в вызывающем коде
    }
}


// Отправка данных в Telegram Web App
export function sendDataToTelegram(data) {
  if (isTelegramWebApp()) {
    window.Telegram.WebApp.sendData(data);
    console.log('Данные отправлены в Telegram Web App:', data);
  } else {
    console.log('Telegram Web App не доступен для отправки данных');
  }
}
