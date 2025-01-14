<template>
  <section class="course-details-section">
    <div class="course-details-left">
      <SidebarMenu :courseId="$route.params.courseId" />
    </div>
    <div class="course-details-right">
      <router-view />
    </div>
  </section>
</template>

<script>
// import TopBar from '../components/TopBar.vue';
import SidebarMenu from '../components/SidebarMenu.vue';

export default {
  components: {
    // TopBar,
    SidebarMenu,
  },
  methods:{
    isAuthenticated() {
      const token = localStorage.getItem('token');
      if (!token || token === '') {
    this.$router.push('/');
  }
    },
  },mounted() {
    this.isAuthenticated();
  }
  };

</script>

<style>

.course-details-section {
  opacity: 1;
  -webkit-text-fill-color: inherit;
  cursor: auto;
  mix-blend-mode: normal;
  background-clip: border-box;
  flex-flow: row;
  justify-content: flex-start;
  align-items: stretch;
  height: auto;
  margin-top: 10vh;
  margin-bottom: 10vh;
  margin-left: 0;
  padding-bottom: 10vh;
  padding-left: 0;
  display: flex;
  position: static;
  overflow: visible;
}

.course-details-left {
  z-index: 50;
  background-color: rgba(177, 177, 177, .3);
  flex-flow: column;
  justify-content: flex-start;
  width: 20%;
  height: 100%;
  padding-top: 1%;
  padding-left: 0%;
  padding-right: 0%;
  display: block;
  position: fixed;
  left: 0%;
  top: 10vh;
  overflow: visible;
}

.course-details-right {
  z-index: 50;
  width: 80%;
  height: 100%;
  margin-left: 20%;
  padding-top: 1%;
  padding-bottom: 1%;
  position: relative;
  top: 0;
  left: 0;
  overflow: auto;
}
</style>
