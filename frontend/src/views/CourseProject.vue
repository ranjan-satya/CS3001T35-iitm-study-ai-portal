<template>
  <div>
    <h3>About the Course</h3>
    <div v-if="course">
      <p>{{ course.about }}</p>
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
      api.get(`/course/${courseId}/about`)
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
</style>
