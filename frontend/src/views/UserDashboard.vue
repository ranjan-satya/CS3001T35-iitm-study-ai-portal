<template>
  <section class="dashboard-content-section">
    <div class="dashboard-content-left">
        <div class="dashboard-search-comp">
            <div class="form-block w-form">
                <form id="search-form" name="search-form" data-name="Email Form" method="get"
                    class="dashboard-search-form" data-wf-page-id="669fb346fc936492f41a84ec"
                    data-wf-element-id="16a2212a-f63b-5a54-5657-6a11ccdc6eaa"><input
                        class="dashboard-search-box w-input" maxlength="256" name="name" data-name="Name"
                        placeholder="" type="text" id="name" /><input type="submit" data-wait="Please wait..."
                        class="dashboard-search-submit w-button" value="Search" />
                  </form>
            </div>
        </div>
        <div class="dashboard-filters-comp">
            <h3 class="dashboard-filter-title">Filters</h3>
        </div>
    </div>
    <div class="dashboard-content-right">
      <div class="dashboard-enrolled-courses">
        <h1 class="dahsboard-courses-section-title">Enrolled courses</h1>
        <div class="dashboard-card-wrapper">
          <template v-for="(course,index) in courses" :key="course.course_id">
            <div v-if="enrollment_status[index]" class="darshboard-card" >
              
                <img :src="require(`../assets/${course_banners[index]}`)"
                loading="lazy" width="270"
                sizes="(max-width: 479px) 154.640625px, (max-width: 991px) 32vw, 268px" alt=""
                class="dashboard-card-banner" />
                <div class="dashboard-card-content">
                  <h3 class="dashboard-card-title">{{ course.course_name }}</h3>
                  <button class="dashboard-go-to-course-button w-button" @click="showCourseDetails(course)" >Go to course page</button>   
                </div>
              
            </div>
          </template>
        </div>
      </div>
      <div class="dashboard-explore-courses">
        <h1 class="dahsboard-courses-section-title">Explore more courses</h1>
        <div class="dashboard-card-wrapper">
          <template v-for="(course,index) in courses" :key="course.course_id">
            <div class="darshboard-card" v-if="!enrollment_status[index]">
                <img
                :src="require(`../assets/${course_banners[index]}`)"
                loading="lazy" width="270"
                sizes="(max-width: 479px) 92.109375px, (max-width: 767px) 19vw, 21vw" alt=""
                class="dashboard-card-banner" />
                <div class="dashboard-card-content">
                  <h3 class="dashboard-card-title">{{ course.course_name }}</h3>
                  <button class="dashboard-go-to-course-button w-button" @click="showCourseDetails(course)">Go to course page</button>
                </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import api from '../axios';

export default {
  data() {
    return {
      courses: [],
      enrollment_status: [true, true, true, true, true],
      course_banners: ['SE_banner.jpg','deep-learning-banner.jpg','ai-smps-banner.jpg','cv-banner.jpg','data-viz-banner.jpg']
    };
  },
  methods: {
    fetchCourses() {
      api.get('/courses')
        .then(response => {
          this.courses = response.data.courses;
        })
        .catch(error => {
          console.error('Error fetching courses:', error);
        });
    },
    showCourseDetails(course) {
      console.log(course)
      this.$router.push({ name: 'CourseAbout', params: { courseId: course.course_id } });
    },
    isAuthenticated() {
  const token = localStorage.getItem('token');

  if (!token || token === '') {
    this.$router.push('/');
  }
},
  },
  mounted() {
    this.fetchCourses();
    this.isAuthenticated();
  }
};
</script>

<style scoped>
.dashboard-content-section {
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

.dashboard-card-content {
  flex-flow: column;
  align-items: center;
  padding: 0 10px 15px;
  display: flex;
}

.dashboard-card-title {
  color: #000;
  text-align: center;
  align-self: center;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

.dashboard-content-left {
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
  overflow: visible;
}

.dashboard-card-banner {
  border-radius: 20px 20px 0 0;
}

.dashboard-go-to-course-button {
  background-color: var(--iitm-theme-yellow);
  color: var(--white);
  cursor: pointer;
  border-radius: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.dashboard-search-comp {
  margin-top: 24px;
  padding: 7%;
}

.form-block {
  margin-bottom: 0;
}

.dashboard-search-form {
  align-items: baseline;
  display: flex;
}

.dashboard-search-box {
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  height: 100%;
}

.dashboard-search-submit {
  color: var(--grey);
  cursor: pointer;
  background-color: #fff;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  height: 100%;
  padding: 6px 10px;
}

.dashboard-filters-comp {
  padding: 0% 7% 7%;
}

.dashboard-filter-title {
  margin-top: 10px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.dashboard-content-right {
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

.dashboard-enrolled-courses, .dashboard-explore-courses {
  height: auto;
  padding-left: 5%;
  padding-right: 5%;
}

.dahsboard-courses-section-title {
  padding-left: 0%;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.dashboard-card-wrapper {
  display: flex;
  overflow: visible;
}

.darshboard-card {
  background-color: var(--white);
  border: .5px solid #dadada;
  border-radius: 20px;
  flex-flow: column;
  width: 270px;
  margin-left: 0;
  margin-right: 30px;
  padding: 0;
  display: flex;
  box-shadow: 5px 5px 11px rgba(0, 0, 0, .2);
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  grid-gap: 20px;
}

.course-box {
  cursor: pointer;
}

.card {
  height: 100%;
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #8a2be2;
  color: white;
}

.card-body {
  text-align: center;
  padding: 20px;
  font-size: 18px;
}

.no-courses {
  text-align: center;
  margin-top: 20px;
  color: #666;
}
</style>
