<template>
    <main>
        <OrderTable />
    </main>
</template>


<script setup>
import OrderTable from '@/components/OrderTable/OrderTable.vue';
</script>

<style scoped>
main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: inherit;
    position: relative;

}
</style>