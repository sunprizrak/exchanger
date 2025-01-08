<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
    <header>

        <div class="wrapper">
            <HelloWorld msg="Бобёр скуф!" />
            <h1 class="text-3xl font-bold underline">ki!</h1>
            <nav>
                <RouterLink to="/">Home</RouterLink>
                <router-link to="/" v-if="myUser">{{ myUser.email }}</router-link>
            </nav>
        </div>
    </header>

  <RouterView />
</template>

<script>
  import gql from "graphql-tag";

  export default {
    data() {
      return {
        myUser: null,
      };
    },

    async created() {
      const UserInfo = await this.$apollo.query({
        query: gql`
          query {
            user {
              email
            }
          }
        `,
      });
      this.myUser = UserInfo.data.user;
    },
  };

</script>

<style scoped>
header {
    line-height: 1.5;
    max-height: 100vh;
}

header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
}

</style>
