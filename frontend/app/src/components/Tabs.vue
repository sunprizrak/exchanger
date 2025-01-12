<template>
  <div class="wrapper">
    <h2>Пример вкладок</h2>
    <ul class="tabs">
      <li>
        <a href="#" :class="{'active': activeTab === 1}" @click="setActiveTab(1)">Таб 1</a>
      </li>
      <li>
        <a href="#" :class="{'active': activeTab === 2}" @click="setActiveTab(2)">Таб 2</a>
      </li>
      <li>
        <a href="#" :class="{'active': activeTab === 3}" @click="setActiveTab(3)">Таб 3</a>
      </li>
      <span class="selector"></span>
    </ul>
    <h6>Здесь будет отображаться контент активной вкладки</h6>
  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';

const activeTab = ref(1); // Изначально активна первая вкладка

const setActiveTab = (tabIndex) => {
  activeTab.value = tabIndex;
};

onMounted(() => {
  const tabs = document.querySelector('.tabs');
  const activeItem = tabs.querySelector('.active');
  const activeWidth = activeItem ? activeItem.offsetWidth : 0;
  const itemPos = activeItem ? activeItem.getBoundingClientRect() : { left: 0 };

  const selector = document.querySelector('.selector');
  if (selector && activeItem) {
    selector.style.left = `${itemPos.left}px`;
    selector.style.width = `${activeWidth}px`;
  }
});
</script>


<style scoped>
h2 {
  margin: 0px;
  text-transform: uppercase;
}

h6 {
  margin: 0px;
  color: #777;
}

.wrapper {
  text-align: center;
  margin: 50px auto;
}

.tabs {
  margin-top: 50px;
  font-size: 15px;
  padding: 0px;
  list-style: none;
  background: #fff;
  box-shadow: 0px 5px 20px rgba(0, 0, 0, 0.1);
  display: inline-block;
  border-radius: 50px;
  position: relative;
}

.tabs a {
  text-decoration: none;
  color: #777;
  text-transform: uppercase;
  padding: 10px 20px;
  display: inline-block;
  position: relative;
  z-index: 1;
  transition-duration: 0.6s;
}

.tabs a.active {
  color: #fff;
}

.tabs a i {
  margin-right: 5px;
}

.tabs .selector {
  height: 100%;
  display: inline-block;
  position: absolute;
  left: 0px;
  top: 0px;
  z-index: 1;
  border-radius: 50px;
  transition-duration: 0.6s;
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  background: #05abe0;
  background: -moz-linear-gradient(45deg, #05abe0 0%, #8200f4 100%);
  background: -webkit-linear-gradient(45deg, #05abe0 0%, #8200f4 100%);
  background: linear-gradient(45deg, #05abe0 0%, #8200f4 100%);
  filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#05abe0', endColorstr='#8200f4', GradientType=1);
}
</style>

