<template>
  <div v-if="course">
          <div class="course-ppa-queation-component">
              <h2 class="course-ga-heading">{{ course.exam_name }}</h2>
          </div>
          <h4 v-if="dueDatePassed" class="course-ppa-deadline-text">Due Date for this assignment has already passed</h4>
          <h4 v-else class="course-ppa-deadline-text"> Due date for this assignment: {{ dueDateString }}</h4>
          <div class="course-ppa-component">
              <div class="form-block-2 w-form">
                      <div class="course-ppa-wrapper">   
                          <div class="course-ppa-question-block">
                              <label for="name" class="course-ppa-question" >Q. {{ course.questions[0].question_text }}</label>
                          </div>
                          <div class="course-ppa-answer-block">
                              <div class="courses-ppa-answer">
                                  <p class="course-ppa-solution-titile">
                                      Write your solution here.
                                  </p>
                                  <code-editor :value="code" v-model="code" @written="handleCodeInput"></code-editor>
                                  <div v-if="results.length > 0" class="course-ppa-test-case-result">{{ passedTestCases }} / {{ results.length }} test cases passed.</div>
                                  <div v-if="codeError">
                                    <p class="course-ppa-test-case-error">{{ codeError.message }}</p>
                                    <p class="course-ppa-test-case-error">{{ codeError.traceback }}</p>
                                  </div>
                                  <div class="course-ppa-test-case-title">Test Cases</div>
                                  <div class="course-ppa-test-case-wrapper">
                                    <div class="course-ppa-test-case-header-row">
                                        <div class="course-ppa-test-case-header">
                                            <div class="course-ppa-test-case-header-text">
                                                Input
                                            </div>
                                        </div>
                                        <div class="course-ppa-test-case-header">
                                            <div class="course-ppa-test-case-header-text">
                                                Expected Output
                                            </div>
                                        </div>
                                        <div class="course-ppa-test-case-header">
                                            <div class="course-ppa-test-case-header-text" >
                                                Actual Output
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="results.length === 0">
                                      <div v-for="(option) in course.questions[0].options" :key="option.option_id" class="course-ppa-test-case-row">
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text" style="padding-left: 5%;">
                                                <span v-for="(v, k) in option.sample_input" :key="k" style="padding-right: 10px;">{{k}} = {{ v }}</span>
                                              </div>
                                          </div>
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text" style="padding-left: 5%;">
                                                  {{ option.expected_output }}
                                              </div>
                                          </div>
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text">
                                                  
                                              </div>
                                          </div>
                                      </div>
                                    </div>
                                    <div v-else>
                                      <div v-for="(result,index) in results" :key="index" class="course-ppa-test-case-row">
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text" style="padding-left: 5%;">
                                                  <span v-for="(v, k) in result.input" :key="k" style="padding-right: 10px;">{{k}} = {{ v }}</span>
                                              </div>
                                          </div>
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text" style="padding-left: 5%;">
                                                  {{ result.expected_output }}
                                              </div>
                                          </div>
                                          <div class="course-ppa-test-case">
                                              <div class="course-ppa-test-case-text" style="padding-left: 40%;">
                                                  {{ result.actual_output }}
                                              </div>
                                          </div>
                                      </div>
                                    </div>
                                  </div>
                              </div>
                              <div v-if="showaip">
                              <div class="courses-ppa-genai-block">
                                  <p class="course-ppa-genai-titile">
                                      Interact with AI Agent
                                  </p>
                                  <img @click.prevent="closeai()" src="../assets/icons8-cross-50.png" class="course-ppa-genai-block-close-image">
                                  <div v-if="oldExplanation.length > 1">
                                    <div v-for="(expl,index) in oldExplanation" :key="index">
                                      <div v-if="expl">
                                        <p class="course-ppa-genai-question">
                                          {{expl.query}}
                                        </p>
                                        <p v-if="expl.explanation" class="course-ppa-genai-response">
                                          {{expl.explanation}}
                                        </p>
                                        <p v-if="expl.answer" class="course-ppa-genai-code-response" v-html="convertToHtmlEntities(expl.answer)">
                                        </p>
                                      </div>
                                    </div>
                                  </div>
                                  <div v-if="explanation">
                                    <p class="course-ppa-genai-question">
                                      {{this.explanation.query}}
                                    </p>
                                    <p v-if="explanationDisplayText.explanation" class="course-ppa-genai-response">
                                      {{this.explanationDisplayText.explanation}}
                                    </p>
                                    <p v-if="explanationDisplayText.answer" class="course-ppa-genai-code-response" v-html="convertToHtmlEntities(this.explanationDisplayText.answer)">
                                    </p>
                                  </div>
                                  <v-skeleton-loader v-if="showLoader" type="paragraph" height="100px"
                                    width="100%" class="custom-skeleton-loader"></v-skeleton-loader>
                                  <textarea placeholder="Ask AI" maxlength="5000" id="field-2" name="field-2"
                                      data-name="Field 2" class="course-ppa-genai-input w-input" v-model="query"></textarea><a
                                      href="#" class="button w-button" @click.prevent="genaicode(course.questions[0].question_text)">Ask</a>
                              </div>
                          </div>
                      </div>
                    </div>
                      <button v-if="dueDatePassed" class="course-ppa-submit-button-disable w-button" disabled>Submit</button>
                      <button v-else class="course-ppa-submit-button w-button" @click="submitAnswers()">Submit</button>
                      <button v-if="!showaip" class="course-ppa-genai-button w-button" @click="showai()">Get help from AI</button>
              </div>
          </div>
  </div>
  <v-skeleton-loader v-else type="article" height="400px"
              width="70%" class="custom-skeleton-loader"></v-skeleton-loader>
</template>

<script>
import api from '../axios';
import codeEditor from '../components/codeEditor.vue';

export default {
data() {
  return {
    course: null,
    results: [],
    showLoader: false,
    codeError: null,
    feedback: {},
    showaip:false,
    dummy:{},
    query:"",
    oldExplanation: [],
    explanation:null,
    explanationwords: {},
    explanationDisplayText: {},
    currentWordIndex: 0,
    intervalId: null,
    code: `# This is a read-only section
a = int(input())
b = int(input())
def multiplyNumbers(num1,num2):
# Please do not change any of the above code. Start writing below this line.


# end of code
print(multiplyNumbers(a,b))

`,
  };
},
computed:{
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
    passedTestCases(){
      let count = 0;
      for (let res of this.results) {
          if (res.is_correct) {
            count++;
        }
      }
      return count
    }
  
},
components: {
    codeEditor
  },
methods: {
  showai(){
    this.showaip = true
  },
  closeai(){
    this.showaip = false
  },
  genaicode(question) {
    this.showLoader = true;
    this.oldExplanation.push(this.explanation);
    this.explanation = null;
    this.explanationDisplayText= {answer: '', explanation: ''},
    this.explanationwords= {answer: [], explanation: []},
    api.post(`/genaicode`,{"question":question,"query":this.query,"code":this.code})
      .then(response => {
        this.explanation = response.data;
        this.showLoader = false;
        this.query = "";
        this.startExplanationReveal();
      })
      .catch(error => {
        console.error('Error fetching course details:', error);
      });
  },
  startExplanationReveal() {
      let wordsArray = this.explanation.explanation.split(' ');
      this.explanationwords.explanation = wordsArray;
      this.currentWordIndex = 0;
      this.explanationDisplayText.explanation = "";
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      this.intervalId = setInterval(() => this.revealExplanationNextWord(), 100); // Adjust the interval as needed
    },
    revealExplanationNextWord() {
      if (this.currentWordIndex < this.explanationwords.explanation.length) {
        this.explanationDisplayText.explanation += (this.currentWordIndex > 0 ? ' ' : '') + this.explanationwords.explanation[this.currentWordIndex];
        this.currentWordIndex++;
      } else {
        clearInterval(this.intervalId);
        this.startAnswerReveal();
      }
    },
    startAnswerReveal() {
      let wordsArray = this.explanation.answer.split(' ');
      this.explanationwords.answer = wordsArray;
      this.currentWordIndex = 0;
      this.explanationDisplayText.answer = "";
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      this.intervalId = setInterval(() => this.revealAnswerNextWord(), 100); // Adjust the interval as needed
    },
    revealAnswerNextWord() {
      if (this.currentWordIndex < this.explanationwords.answer.length) {
        this.explanationDisplayText.answer += (this.currentWordIndex > 0 ? ' ' : '') + this.explanationwords.answer[this.currentWordIndex];
        this.currentWordIndex++;
      } else {
        clearInterval(this.intervalId);
      }
    },
  fetchCourseDetails(courseId, weekId) {
    api.get(`/course/${courseId}/week/${weekId}/assignmentexam/0`)
      .then(response => {
        this.course = response.data;
        for(let option of this.course.questions[0].options){
          option.sample_input = JSON.parse(option.sample_input)
        }
      })
      .catch(error => {
        console.error('Error fetching course details:', error);
      });
  },
  handleCodeInput(newCode){
      this.code = newCode;
    },
  submitAnswers() {
    this.results = [];
    this.codeError = null;
    // Send userAnswers to the backend
    api.post('/submit-code', {
      question_id: this.course.questions[0].question_id,
      code: this.code,
    })
    .then(response => {
      this.results = response.data.results; // Assuming backend sends feedback
    })
    .catch(error => {
      if (error.response && error.response.status === 500) {
        this.codeError = { message: error.response.data.message,
          traceback: error.response.data.traceback};
      } else {
        console.error('Error submitting answers:', error);
      }
    });
  },
    isAuthenticated() {
    const token = localStorage.getItem('token');

    if (!token || token === '') {
      this.$router.push('/');
    }
  },
  convertToHtmlEntities(str) {
    if (!str) return '';
    return str
      .replace(/\n/g, '<br>')
      .replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;')
      .replace(/ /g, '&nbsp;');
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
@font-face {
  font-family: webflow-icons;
  src: url("data:application/x-font-ttf;charset=utf-8;base64,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") format("truetype");
  font-weight: normal;
  font-style: normal;
}

[class^="w-icon-"], [class*=" w-icon-"] {
  speak: none;
  font-variant: normal;
  text-transform: none;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  font-style: normal;
  font-weight: normal;
  line-height: 1;
  font-family: webflow-icons !important;
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
input.w-button {
  -webkit-appearance: button;
}


.w-form {
  margin: 0 0 15px;
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

.w-input::placeholder, .w-select::placeholder {
  color: #999;
}

.w-input:focus, .w-select:focus {
  border-color: #3898ec;
  outline: 0;
}
:root {
  --iitm-theme-red: #8f2c2c;
  --grey: #6d6d6d;
  --iitm-theme-yellow: #d3a248;
  --red-low-opacity: rgba(117, 22, 22, .7);
  --white: white;
  --black: black;
  --light-yellow: rgba(216, 161, 59, .56);
}

.course-ga-heading {
  margin-left: 0;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.course-ppa-submit-button-disable {
  background-color: #979797;
  vertical-align: baseline;
  cursor: not-allowed;
  border-radius: 20px;
  margin-top: 20px;
  margin-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

.course-ppa-queation-component {
  height: 5%;
  margin-left: 40px;
  padding-right: 30px;
}


.course-ppa-component {
  object-fit: fill;
  justify-content: space-between;
  height: 100%;
  max-height: none;
  margin-left: 40px;
  margin-right: 40px;
  padding-right: 17px;
  display: flex;
  overflow: visible;
}

.course-ppa-question {
  margin-top: 17px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-size: 16px;
  font-weight: 400;
}

.course-ppa-deadline-text{
  font-family: Ubuntu, Helvetica, sans-serif;
  padding-left: 3.8%;
  padding-top: 1%;
  color:  rgb(255, 0, 0) ;
}

.course-ppa-genai-button {
  background-color: #d3a248;
  vertical-align: baseline;
  cursor: pointer;
  border-radius: 20px;
  margin-top: 20px;
  margin-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

.form-block-2 {
  background-color: #fff;
  height: auto;
}

.course-ppa-wrapper {
  margin-left: 12px;
  padding: 5px;
}

.course-ppa-answer-input {
  background-color: #e7e7e7;
  border-radius: 7px;
  order: 0;
  align-self: stretch;
  width: 100%;
  min-height: 400px;
  overflow: visible;
}

.courses-ppa-answer {
  background-color: rgba(231, 231, 231, .55);
  border-radius: 19px;
  flex-flow: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 55%;
  height: auto;
  margin-top: 10px;
  margin-left: 0;
  padding: 20px;
  display: flex;
  overflow: visible;
}

.button {
  background-color: #d3a248;
  cursor: pointer;
  border-radius: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.course-ppa-solution-titile {
  text-align: justify;
  padding: 4px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 700;
}


.course-ppa-question-block {
  margin-bottom: 30px;
  padding-right: 30px;
  width: 70vw;
}

.course-ppa-answer-block {
  justify-content: space-between;
  align-items: flex-start;
  display: flex;
  position: relative;
  overflow: visible;
}

.courses-ppa-genai-block {
  background-color: rgba(231, 231, 231, 0);
  border: 1px #c9c9c9;
  border-radius: 20px;
  flex-flow: column;
  justify-content: flex-start;
  align-items: flex-start;
  width: 40%;
  min-height: auto;
  max-height: none;
  margin-top: 10px;
  margin-left: 10px;
  padding: 20px;
  display: flex;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: auto;
  right: 0%;
  overflow: auto;
  box-shadow: 4px 4px 15px rgba(0, 0, 0, .2);
}

.course-ppa-test-case-title {
  padding-top: 10px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 700;
}

.course-ppa-test-case-result {
  padding-top: 10px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
  color: #6d6d6d;
}

.course-ppa-test-case-error {
  padding-top: 10px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
  color: #ff5555;
}

.course-ppa-genai-titile {
  text-align: justify;
  align-self: center;
  padding: 4px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 700;
}

.course-ppa-genai-response {
  text-align: left;
  padding: 4px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 300;
}

.course-ppa-genai-question {
  text-align: left;
  padding: 4px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.course-ppa-test-case-wrapper {
  flex-flow: column;
  width: 100%;
  padding-left: 10px;
  padding-right: 10px;
  display: block;
}
.custom-skeleton-loader {
  /* Custom styles for the skeleton loader */
  border-radius: 8px;
  opacity: 0.8;
}

.course-ppa-test-case-header-row {
  border: 1px #000;
  justify-content: space-between;
  width: 100%;
  padding-top: 7px;
  padding-bottom: 7px;
  display: flex;
}

.course-ppa-test-case-header-text {
  font-family: Ubuntu, Helvetica, sans-serif;
}

.course-ppa-test-case-header {
  background-color: #e7e7e7;
  border: 1px #000;
  border-radius: 5px;
  padding: 8px 13px;
}

.course-ppa-test-case-row {
  justify-content: space-between;
  width: 100%;
  padding-top: 8px;
  padding-bottom: 8px;
  display: flex;
}

.course-ppa-test-case {
  color: #7a7a7a;
  font-weight: 400;
  width: 30%;
  overflow: auto;
}

.course-ppa-test-case-text {
  font-family: Ubuntu, Helvetica, sans-serif;
}

.course-ppa-genai-input {
  background-color: #e7e7e7;
  border-radius: 7px;
  order: 0;
  align-self: stretch;
  width: 100%;
  height: 34px;
  min-height: 100px;
  overflow: visible;
}

.course-ppa-submit-button {
  background-color: #8f2c2c;
  vertical-align: baseline;
  cursor: pointer;
  border-radius: 20px;
  margin-top: 20px;
  margin-left: 20px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 500;
}

.course-ppa-genai-code-response {
  text-align: left;
  background-color: #f3f3f3;
  padding: 10px;
  font-family: Inconsolata, monospace;
  font-weight: 400;
  width: 475px;
  overflow-x: auto;

}
.course-ppa-genai-block-close-image{
  position: absolute;
  top: 2%;
  bottom: auto;
  left: auto;
  right: 2.5%;
  cursor: pointer;
  width: 30px;
  height: auto;
}
</style>
