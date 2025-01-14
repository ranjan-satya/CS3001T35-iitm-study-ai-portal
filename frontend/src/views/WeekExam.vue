<template>
    <div v-if="course" class="course-ga-component">
      <h3 class="course-ga-heading" >{{ course.exam_name }}</h3>
      <div class="course-ga-question-component">
      <h4 v-if="dueDatePassed" class="course-ga-deadline-text">Due Date for this assignment has already passed</h4>
      <h4 v-else class="course-ga-deadline-text"> Due date for this assignment: {{ dueDateString }}</h4>
      <div class="form-block-2 w-form">
          <div v-for="(i,i_index) in course.questions" :key="i.question_id">  
            <div class="course-ga-question-wrapper">
            
              <p class="course-ga-question"> Q{{ i_index + 1 }}. {{ i.question_text }} </p>
              <div class="course-ga-options">
                <label class="course-ga-option-wrapper w-radio" v-for="(j, index) in i.options" :key="index">
                  <input 
                    type="radio" 
                    :name="'options-for-'+i.question_id" 
                    :id="'option-' + i.question_id + '-' + index" 
                    :data-name="'option' + '-for-q' + i.question_id" 
                    class="w-form-formradioinput w-radio-input" 
                    :value="{question_id: i.question_id, selected_option_id: j.option_id}"
                    v-model="selectedOptions[i.question_id]"
                  />
                  <span class="course-ga-option w-form-label" :for="'option-' + i.question_id + '-' + index">{{ j.option_text }}</span>
                </label>
              </div>
                      
            <div class="courses-ga-genai-block">
              <div v-if="oldDummy[i.question_id]">
                <div v-for="(dum,dum_index) in oldDummy[i.question_id]" :key="dum_index">
                  <p class="paragraph" :style="{ fontSize: '16px', fontWeight: '500' }">{{ dum.query }}</p>
                  <p class="paragraph"> {{ dum.answer }}</p>
                  <p class="paragraph"> {{ dum.explanation }}</p>
                </div>
              </div>
              <div  v-if="dummy[i.question_id]">
                <p v-if="i.question_id==dummy[i.question_id].qid" class="paragraph" :style="{ fontSize: '16px', fontWeight: '500' }">{{ dummy[i.question_id].query }}</p>
                <p v-if="i.question_id==dummy[i.question_id].qid" class="paragraph"> {{ dummyDisplayText[i.question_id].answer }}</p>
                <p v-if="i.question_id==dummy[i.question_id].qid" class="paragraph"> {{ dummyDisplayText[i.question_id].explanation }}</p>
              </div>
            
              <v-skeleton-loader v-if="showLoader[i_index]" type="paragraph" height="100px"
              width="100%" class="custom-skeleton-loader"></v-skeleton-loader>
            
              <textarea 
                placeholder="Ask AI"
                maxlength="5000"
                id="field-2"
                name="field-2"
                data-name="Field 2"
                class="textarea w-input"
                v-model="userquery[i.question_id]"
              ></textarea>
              <button class="button w-button" @click="dummyapi(i.question_text,i.question_id,i_index)">Ask</button>
            
            </div>
            </div>
          </div>
          <button v-if="dueDatePassed" class="submit-button-disabled w-button" disabled>Submit</button>
          <button v-else class="submit-button w-button" @click="submitAnswers()">Submit</button>
          <div v-if="score !==  null">
            <p class="course-ga-score">Your Score is : {{ score }}/{{ course.questions.length }} </p>
          </div>
      </div>
  </div>
</div>
<v-skeleton-loader v-else type="article" height="400px"
              width="70%" class="custom-skeleton-loader"></v-skeleton-loader>
</template>
<script>
import api from '../axios';

export default {
  data() {
    return {
      course: null,
      feedback: {},
      showLoader: [],
      userquery:{},
      selectedOptions:{},
      score: null,
      percentage: null,
      oldDummy: {},
      dummy:{},
      dummywords: {},
      dummyDisplayText: {},
      currentWordIndex: 0,
      intervalId: null
      
    };
  },
  computed:{
    user_answers(){
      return Object.values(this.selectedOptions);
    },
    due_date(){
      const dueDateObject = new Date(this.course.exam_end_time);
      const offsetIST = 5.5 * 60;
      const istDueDateObject = new Date(dueDateObject.getTime() + offsetIST * 60 * 1000);
      return istDueDateObject
    },
    dueDateString(){
      const date = this.due_date;
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
      const day = String(date.getDate()).padStart(2, '0');
      const hours = String(date.getHours()).padStart(2, '0');
      const minutes = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day}, ${hours}:${minutes} IST`;
    },
    dueDatePassed(){
      const currentDate = new Date();
      return this.due_date.getTime() < currentDate.getTime();
    },
  },
  methods: {
    fetchCourseDetails(courseId, weekId) {
      api.get(`/course/${courseId}/week/${weekId}/exam/0`)
        .then(response => {
          this.course = response.data;
          let numOfQuestions = this.course.questions.length;
          this.showLoader = new Array(numOfQuestions).fill(false);
        })
        .catch(error => {
          console.error('Error fetching course details:', error);
        });
    },
    submitAnswers() {
    api.post(`/submit-answers`,{
      course_id: this.course.course_id,
      exam_id: this.course.exam_id,
      user_answers: this.user_answers
    })
      .then(response => {
        this.score = response.data.score
        this.percentage = response.data.percentage
      })
    },
    dummyapi(question,id,index) {
      this.showLoader[index] = true;
      if (this.oldDummy[id] === undefined) {
        this.oldDummy[id] = [];
      }else{
        if(this.dummy[id] === undefined){
          this.oldDummy[id].push(null);
        }else{
          this.oldDummy[id].push(this.dummy[id]);
        }
      }
      this.dummy[id] = null;
      this.dummyDisplayText[id]= {answer: '', explanation: ''},
      this.dummywords[id]= {answer: [], explanation: []},
      api.post(`/dummy`,{query:this.userquery[id],ans:this.selectedOptions[id],question:question,qid:id})
        .then(response => {
          this.dummy[id] = response.data;
          this.showLoader[index] = false;
          this.userquery[id] = '';
          this.startAnswerReveal(id);
        })
        .catch(error => {
          console.error('Error fetching course details:', error);
        });
    },
    startAnswerReveal(id) {
      let wordsArray = this.dummy[id].answer.split(' ');
      wordsArray.unshift('Answer:');
      this.dummywords[id].answer = wordsArray;
      this.currentWordIndex = 0;
      this.dummyDisplayText[id].answer = "";
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      this.intervalId = setInterval(() => this.revealAnswerNextWord(id), 100); // Adjust the interval as needed
    },
    revealAnswerNextWord(id) {
      if (this.currentWordIndex < this.dummywords[id].answer.length) {
        this.dummyDisplayText[id].answer += (this.currentWordIndex > 0 ? ' ' : '') + this.dummywords[id].answer[this.currentWordIndex];
        this.currentWordIndex++;
      } else {
        clearInterval(this.intervalId);
        this.startExplanationReveal(id);
      }
    },
    startExplanationReveal(id) {
      let wordsArray = this.dummy[id].explanation.split(' ');
      wordsArray.unshift('Explanation:');
      this.dummywords[id].explanation = wordsArray;
      this.currentWordIndex = 0;
      this.dummyDisplayText[id].explanation = "";
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      this.intervalId = setInterval(() => this.revealExplanationNextWord(id), 100); // Adjust the interval as needed
    },
    revealExplanationNextWord(id) {
      if (this.currentWordIndex < this.dummywords[id].explanation.length) {
        this.dummyDisplayText[id].explanation += (this.currentWordIndex > 0 ? ' ' : '') + this.dummywords[id].explanation[this.currentWordIndex];
        this.currentWordIndex++;
      } else {
        clearInterval(this.intervalId);
      }
    },
    isAuthenticated() {
    const token = localStorage.getItem('token');

    if (!token || token === '') {
      this.$router.push('/');
    }
    },
  },
  mounted() {
    const { courseId, weekId } = this.$route.params;
    this.fetchCourseDetails(courseId, weekId);
    this.isAuthenticated();
  }
};
</script>

<style scoped>

.custom-skeleton-loader {
  /* Custom styles for the skeleton loader */
  border-radius: 8px;
  opacity: 0.8;
  margin-bottom: 10px;
}

.course-details-right {
    z-index: 50;
    width: 80%;
    height: 100%;
    margin-left: 20%;
    padding-top: 1%;
    position: relative;
    top: 0;
    left: 0;
    overflow: auto;
  }
.paragraph {
  padding: 4px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.w-form-done {
  text-align: center;
  background-color: #ddd;
  padding: 20px;
  display: none;
}
.w-form-fail {
  background-color: #ffdede;
  margin-top: 10px;
  padding: 10px;
  display: none;
}
.course-ga-component {
    height: 5%;
    margin-left: 40px;
    padding-right: 30px;
  }
.course-ga-heading {
    margin-left: 0;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-weight: 300;
    font-size: 32px;
  }

.course-ga-score{
  font-family: Ubuntu, Helvetica, sans-serif;
  padding-left: 2%;
  padding-top: 1%;
  color:  rgb(138, 138, 138) ;
}

.course-ga-deadline-text{
  font-family: Ubuntu, Helvetica, sans-serif;
  padding-top: 1%;
  color:  rgb(255, 0, 0) ;
}

.course-ga-options {
    margin-top: 12px;
    padding-left: 12px;
    font-family: Ubuntu, Helvetica, sans-serif;
  }

.course-ga-question-wrapper {
    margin-left: 12px;
    padding: 5px;
  }
.course-ga-question {
    margin-top: 17px;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-size: 16px;
    font-weight: 400;
  }
.course-ga-question-wrapper {
    margin-left: 12px;
    padding: 5px;
  }

.button {
    background-color: #d3a248;
    cursor: pointer;
    border-radius: 20px;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-weight: 400;
  }
.w-button {
  color: #fff;
  line-height: inherit;
  cursor: pointer;
  background-color: #3898ec;
  border: 0;
  border-radius: 0;
  padding: 9px 15px;
  text-decoration: none;
  display: inline-block;
}
textarea.w-input, textarea.w-select {
  height: auto;
}
textarea {
  overflow: auto;
}
* {
  box-sizing: border-box;
}
.courses-ga-genai-block {
  background-color: rgba(231, 231, 231, .55);
  border-radius: 19px;
  flex-flow: column;
  align-items: flex-start;
  margin-top: 10px;
  margin-left: 10px;
  padding: 20px;
  display: flex;
  max-height: 500px;
  overflow: auto;
}
.course-details-right {
  z-index: 50;
  width: 80%;
  height: 100%;
  margin-left: 20%;
  padding-top: 1%;
  position: relative;
  top: 0;
  left: 0;
  overflow: auto;
}
html {
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
  font-family: sans-serif;
}
body {
  color: #333;
  background-color: #fff;
  min-height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
  font-size: 14px;
  line-height: 20px;
  margin-top: 10vh;
}

h2 {
  margin-top: 20px;
  font-size: 32px;
  line-height: 36px;
}
.w-input, .w-select {
  color: #333;
  vertical-align: middle;
  background-color: #fff;
  border: 1px solid #ccc;
  width: 100%;
  height: 38px;
  margin-bottom: 10px;
  padding: 8px 12px;
  font-size: 14px;
  line-height: 1.42857;
  display: block;
}
.submit-button {
  background-color: #8f2c2c;
  vertical-align: baseline;
  cursor: pointer;
  border-radius: 20px;
  margin-top: 20px;
  margin-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

.submit-button-disabled {
  background-color: #979797;
  vertical-align: baseline;
  cursor: not-allowed;
  border-radius: 20px;
  margin-top: 20px;
  margin-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

form {
    display: block;
    margin-top: 0em;
    unicode-bidi: isolate;
}

.textarea {
  background-color: #e7e7e7;
  border-radius: 7px;
  min-height: 80px;
}
button, input, optgroup, select, textarea {
  color: inherit;
  font: inherit;
  margin: 0;
}


.paragraph {
    padding: 4px;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-weight: 400;
  }
  
.body {
    margin-top: 10vh;
  }

button, input, optgroup, select, textarea {
    color: inherit;
    font: inherit;
    margin: 0;
  }

.button {
    background-color: #d3a248 ;
    cursor: pointer;
    border-radius: 20px;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-weight: 400;
  }
input.w-button {
    -webkit-appearance: button;
  }
  .course-details-right {
  z-index: 50;
  width: 80%;
  height: 100%;
  margin-left: 20%;
  padding-top: 1%;
  position: relative;
  top: 0;
  left: 0;
  overflow: auto;
}
.course-ga-question-component {
  object-fit: fill;
  height: 92%;
  max-height: none;
  margin-right: 40px;
  padding-right: 30px;
  overflow: visible;
}
.course-details-section {
  z-index: -10;
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
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow: visible;
}
.course-ga-question {
  margin-top: 17px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-size: 16px;
  font-weight: 400;
}
.custom-skeleton-loader {
  /* Custom styles for the skeleton loader */
  border-radius: 8px;
  opacity: 0.8;
}
.course-ga-option-wrapper {
  padding-right: 50px;
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
.exam-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 10px;
}


.question-card {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
}

h4 {
  font-size: 16px;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 10px;
}

label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

input[type="radio"] {
  margin-right: 10px;
}

.feedback {
  margin-top: 10px;
}

.correct {
  color: green;
}

.incorrect {
  color: red;
}

.accepted-answer {
  font-weight: bold;
}

</style>
