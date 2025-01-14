import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from './views/UserLogin.vue';
import UserDashboard from './views/UserDashboard.vue';
import CourseDetails from './views/CourseDetails.vue';
import CourseAbout from './views/CourseAbout.vue';
import CourseGeneral from './views/CourseGeneral.vue';
import CoursePleaseRead from './views/CoursePleaseRead.vue';
import CoursePlacement from './views/CoursePlacement.vue';
import CourseProject from './views/CourseProject.vue';
import WeekDemo from './views/WeekDemo.vue';
import WeekExam from './views/WeekExam.vue';
import WeekExamGraded from './views/WeekExamGraded.vue';
import WeekProgramming from './views/WeekProgramming.vue';
import WeekProgrammingGraded from './views/WeekProgrammingGraded.vue';

// Define your routes
const routes = [
  { path: '/', name: 'UserLogin' ,component: UserLogin },
  { path: '/dashboard', component: UserDashboard },
  {
    path: '/course/:courseId',
    name: 'CourseDetails',
    component: CourseDetails,
    children: [
      { path: 'about', component: CourseAbout, name:'CourseAbout' },
      { path: 'general-instructions', component: CourseGeneral },
      { path: 'please-read', component: CoursePleaseRead },
      { path: 'placement-activity', component: CoursePlacement },
      { path: 'course-project', component: CourseProject },
      {
        path: 'week/:weekId/demo',
        name: 'WeekDemo',
        component: WeekDemo
      },
      {
        path: 'week/:weekId/exam',
        name: 'WeekExam',
        component: WeekExam
      },{
        path: 'week/:weekId/gradedexam',
        name: 'WeekGradedExam',
        component: WeekExamGraded
      },
      {
        path: 'week/:weekId/Programmingexam',
        name: 'WeekProgramming',
        component: WeekProgramming
      },
      {
        path: 'week/:weekId/GradedProgrammingexam',
        name: 'WeekProgrammingGraded',
        component: WeekProgrammingGraded
      }
    ]
  }
];

// Create the router instance
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
