<template>
  <div id="app">
    <header-comp></header-comp>
    <router-view></router-view>
    <footer-comp/>
  </div>
</template>

<script>
import FooterComp from './components/footerComp.vue';
import headerComp from './components/headerComp.vue';

export default {
  name: 'App',
  components: { headerComp, FooterComp },

};
</script>

<style>
</style>
