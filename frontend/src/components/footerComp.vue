<template>
    <section class="footer-section">
        <div class="team-details">SE May 2024 (Team-35)</div>
    </section>
</template>

<script>
    export default {
        name: 'footerComp',
}
</script>

<style scoped>
.footer-section {
    z-index: 100;
    background-color: var(--iitm-theme-red);
    justify-content: center;
    align-items: center;
    height: 6vh;
    min-height: 50px;
    display: flex;
    position: fixed;
    top: auto;
    bottom: 0%;
    left: 0%;
    right: 0%;
  }

.team-details {
    color:  #d3a248;
    text-align: center;
    text-transform: uppercase;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-size: 16px;
    font-weight: 500;
}
.footer-section {
  z-index: 100;
  background-color: #8f2c2c;
  justify-content: center;
  align-items: center;
  height: 6vh;
  min-height: 50px;
  display: flex;
  position: fixed;
  top: auto;
  bottom: 0%;
  left: 0%;
  right: 0%;
}
</style>