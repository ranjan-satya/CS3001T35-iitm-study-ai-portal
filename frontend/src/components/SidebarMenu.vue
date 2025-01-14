<template>
  <div>
    <div class="course-details-left-title">
      <h3 class="dashboard-filter-title">Contents</h3>
    </div>
    <div class="course-details-left-list">
      <div class="course-details-left-list-item" >
        <div class="course-details-left-list-item-title link" @click="toggleMenu('courseIntro')">
          <h4 class="course-details-left-list-item-title-name">
          - Course Introduction
          </h4>
          <img
          src="../assets/icons8-right-button-50.png"
          loading="lazy"
          width="20"
          alt=""
          :class="[
            'course-details-left-list-item-title-image',
            { 'rotated': menus.courseIntro }
          ]"
          />
        </div>
        <div v-if="menus.courseIntro" >
          <div class="course-details-left-list-subitem">
            <router-link :to="`/course/${courseId}/about`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              About the course
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/general-instructions`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              General Instructions
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/please-read`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Please Read
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/placement-activity`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Placement Activity
              </h4>
            </router-link>
        </div>
        </div>
      </div>
      <div class="course-details-left-list-item" >
        <div class="course-details-left-list-item-title link" @click="toggleMenu('week1')">
          <h4 class="course-details-left-list-item-title-name">- Week 1</h4>
          <img
          src="../assets/icons8-right-button-50.png"
          loading="lazy"
          width="20"
          alt=""
          :class="[
            'course-details-left-list-item-title-image',
            { 'rotated': menus.week1 }
          ]"
          />
        </div>
        <div v-if="menus.week1">
          <div class="course-details-left-list-subitem">
            <router-link :to="`/course/${courseId}/week/1/demo`" class="link" >
              <h4 class="course-details-left-list-subitem-title">
              Lecture Video
              </h4>
            </router-link>
            
            <router-link :to="`/course/${courseId}/week/1/exam`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Practice Assignment
              </h4>
            </router-link>
            
            <router-link :to="`/course/${courseId}/week/1/gradedexam`" class="link" >
              <h4 class="course-details-left-list-subitem-title">
              Graded Assignment
              </h4>
            </router-link>
            
            <router-link :to="`/course/${courseId}/week/1/Programmingexam`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Practice Programming Assignment 1
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/week/1/Programmingexam`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Practice Programming Assignment 2
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/week/1/GradedProgrammingexam`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Graded Programming Assignment 1
              </h4>
            </router-link>
            <router-link :to="`/course/${courseId}/week/1/GradedProgrammingexam`" class="link">
              <h4 class="course-details-left-list-subitem-title">
              Graded Programming Assignment 2
              </h4>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  props: {
    courseId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      menus: {
        courseIntro: false,
        week1: false,
        week2: false,
        week3: false,
        week4: false
      }
    };
  },
  methods: {
    toggleMenu(menu) {
      this.menus[menu] = !this.menus[menu];
    }
  }
};
</script>

<style>

.dashboard-filter-title {
  text-transform: uppercase;
  margin-top: 10px;
  margin-left: 30px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}
.course-details-left-list {
  padding-left: 7%;
  padding-right: 7%;
}

.rotated {
  transform: rotate(90deg); /* Rotate the image 90 degrees */

}

.course-details-left-list-item-title-name {
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
  cursor: pointer;
}

.course-details-left-list-item-title-image {
  margin-left: 4px;
  padding-left: 0;
}

.course-details-left-list-subitem-title {
  padding-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-size: 16px;
  font-weight: 300;
  cursor: pointer;
}

.course-details-left-list-item-title {
  justify-content: flex-start;
  align-items: center;
  display: flex;
}

.link {
  color: var(--grey);
  cursor: pointer;
  text-decoration: none;
}

.sidebar {
  width: 220px;
  background-color: #343a40;
  color: #fff;
  padding: 20px;
  border-right: 2px solid #495057;
  height: 100vh;
}

.sidebar ul {
  list-style: none;
  padding: 0;
}

.sidebar li {
  margin-bottom: 10px;
}

.menu-item {
  display: block;
  padding: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  text-align: left; /* Align menu items to the left */
}

.menu-item i {
  margin-right: 10px; /* Adjust icon spacing */
}

.menu-item:hover {
  background-color: #495057;
  border-radius: 4px;
}

.sidebar .submenu {
  margin-left: 0; /* Remove default indentation */
  padding-left: 0; /* Remove default padding */
}

.sidebar .submenu li {
  margin-bottom: 8px;
}

.sidebar .submenu li .submenu-link {
  font-size: 14px;
  padding: 8px;
  display: block;
  transition: color 0.3s ease;
  text-align: left; /* Align nested link text to the left */
  color: #fff; /* Set submenu link color to white */
  text-decoration: none; /* Remove underline from submenu links */
}

.sidebar .submenu li .submenu-link:hover {
  color: #007bff; /* Change color on hover */
}
</style>
