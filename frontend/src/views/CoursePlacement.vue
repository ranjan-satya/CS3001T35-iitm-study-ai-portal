<template>
  <div class="course-intro-component">
    <h2 class="course-intro-heading">Placement Activity</h2>
    <div v-if="course">
      <p class="course-intro-paragraph">{{ course.placement_activity }}</p>
    </div>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      course: null
    };
  },
  methods: {
    fetchCourseDetails(courseId) {
      api.get(`/course/${courseId}/placement_activity`)
        .then(response => {
          this.course = response.data;
        })
        .catch(error => {
          console.error('Error fetching course details:', error);
        });
    },
    isAuthenticated() {
      const token = localStorage.getItem('token');
      if (!token || token === '') {
    this.$router.push('/');
  }
    }
  },
  mounted() {
    this.fetchCourseDetails(this.$route.params.courseId);
    this.isAuthenticated();
  }
};
</script>

<style scoped>
/* Component-specific styles if needed */
.course-intro-heading {
  margin-left: 0;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.course-intro-paragraph {
  font-size: 16px;
  padding-right: 20%;
  font-family: Ubuntu, Helvetica, sans-serif;
  padding-top: 1%;
}

.course-intro-component {
  margin-left: 40px;
  padding-right: 30px;
}
</style>
