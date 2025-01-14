<template>
  <div class="course-lecture-component">
    <h2 class="course-lecture-heading ">Lecture</h2>
    <div v-if="course">
      <iframe width="700" height="400" :src="embedUrl" frameborder="0" allowfullscreen class="course-lecture-video-frame"></iframe>
    </div>
    <v-skeleton-loader v-else type="card" height="400px"
              width="70%" class="custom-skeleton-loader"></v-skeleton-loader>
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
  computed: {
    embedUrl() {
      if (this.course && this.course.demo) {
        let videoId = this.extractVideoId(this.course.demo);
        return `https://www.youtube.com/embed/${videoId}`;
      }
      return '';
    }
  },
  methods: {
    fetchCourseDetails(courseId, weekId) {
      api.get(`/course/${courseId}/week/${weekId}/demo`)
        .then(response => {
          this.course = response.data;
        })
        .catch(error => {
          console.error('Error fetching course details:', error);
        });
    },
    extractVideoId(url) {
      let videoId = '';
      if (url.includes('youtube.com')) {
        videoId = url.split('v=')[1];
      } else if (url.includes('youtu.be')) {
        videoId = url.split('/').pop();
      }
      const ampersandPosition = videoId.indexOf('&');
      if (ampersandPosition !== -1) {
        videoId = videoId.substring(0, ampersandPosition);
      }
      return videoId;
    },
    isAuthenticated() {
  const token = localStorage.getItem('token');

  if (!token || token === '') {
    this.$router.push('/');
    this.isAuthenticated();
  }
}
  },
  mounted() {
    const { courseId, weekId } = this.$route.params;
    this.fetchCourseDetails(courseId, weekId);
  }
};
</script>

<style scoped>
/* Component-specific styles if needed */
.course-lecture-component {
  margin-left: 40px;
  padding-right: 30px;
}

.course-lecture-heading {
  margin-left: 0;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.course-lecture-video-frame{
  margin-right: 20%;
  margin-top: 1%;
}

.custom-skeleton-loader {
  /* Custom styles for the skeleton loader */
  border-radius: 8px;
  opacity: 0.8;
}
</style>
