<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
    <main>
        <div>
            <h1>Telegram WebApp Example</h1>
            <div v-if="telegramData">
                <p><strong>id:</strong> {{ tgId }}</p>
                <p><strong>username:</strong> {{ tgUsername }}</p>
            </div>
            <div v-else>
                <p>Данные Telegram WebApp не получены.</p>
            </div>
        </div>
    </main>
</template>


<script>
import { USER_SIGNUP } from "@/mutations";

export default {
  name: "HomeView",

  data() {
    return {
      telegramData: null,
      tgId: null,
      tgUsername: null,
    };
  },

  mounted() {
    const script = document.createElement("script");
    script.src = "https://telegram.org/js/telegram-web-app.js";
    script.onload = () => this.handleSignUp(); // Начинаем процесс регистрации
    document.head.appendChild(script);
  },

  methods: {
    async initializeTelegram() {
      if (window.Telegram && window.Telegram.WebApp) {
        window.Telegram.WebApp.ready();

        this.telegramData = window.Telegram.WebApp.initData || "initData пустой.";
        console.log("Полученные данные:", this.telegramData);

        const urlParams = new URLSearchParams(this.telegramData);
        const userParam = urlParams.get("user");
        if (userParam) {
          try {
            const userData = JSON.parse(decodeURIComponent(userParam));
            this.tgId = String(userData.id);
            this.tgUsername = userData.username;
          } catch (error) {
            console.error("Ошибка декодирования Telegram данных:", error);
          }
        }
      } else {
        console.error("Telegram WebApp API не найден.");
      }
    },

    async userSignUp() {
      if (!this.tgId || !this.tgUsername) {
        console.error("Telegram данные отсутствуют или некорректны.");
        return;
      }

      try {
        const response = await this.$apollo.mutate({
          mutation: USER_SIGNUP,
          variables: {
            tgId: this.tgId,
            tgUsername: this.tgUsername,
          },
        });

        console.log("Пользователь успешно зарегистрирован");
      } catch (error) {
        console.error("Ошибка выполнения мутации:", error);
      }
    },

    async handleSignUp() {
      try {
        // Шаг 1: Инициализация Telegram данных
        await this.initializeTelegram();

        // Шаг 2: Регистрация пользователя
        await this.userSignUp();
      } catch (error) {
        console.error("Ошибка в процессе регистрации:", error);
      }
    },
  },
};
</script>