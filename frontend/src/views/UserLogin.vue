<template>
  <section class="signin-content-section">
    <div class="signin-section">
        <h3 class="signin-title">Sign-in</h3>
        <button class="signin-with-google"><img
                src="../assets/google.svg"
                loading="lazy" width="30" alt="" /><a href="#" class="sign-in-with-google-button w-button">Sign in
                with Google</a></button>
        <p class="signin-or-option">OR</p>
        <div class="sign-in-form-block w-form">
            <form @submit.prevent="submitForm" id="email-form" name="email-form" data-name="Email Form" method="post" class="sign-in-form" data-wf-page-id="669f962e538ee9ed8d3cbcf6" data-wf-element-id="935eb7d0-b033-89a5-4ed2-1254c69c159d">
              <div>
                <label for="email" class="form-label">Student Email</label>
                <input v-model="email" class="signin-text w-input" maxlength="256" name="email" data-name="Email" type="email" id="email" placeholder="Enter your Student Email Id" required />
              </div> 
              <div>
                <label for="password" class="form-label">Password</label>
                <input v-model="password" class="signin-text w-input" maxlength="256" name="password" data-name="Password" placeholder="Enter your password" type="password" id="password" required />
              </div>     
              <button type="submit" data-wait="Please wait..." class="signin-button w-button">Submit</button> 
              <div v-if="status === 'success'" class="alert alert-success mt-4" role="alert">
                {{ message }}
              </div>
              <div v-if="status === 'error'" class="alert alert-danger mt-4" role="alert">
                {{ message }}
              </div>
            </form>
            <div class="signin-success-message w-form-done">
                <div class="success-text">Signing you in.. </div>
            </div>
            <div class="w-form-fail">
                <div>Oops! Something went wrong while submitting the form.</div>
            </div>
        </div>
    </div>
</section>
</template>

<script>
import api from '../axios';
import router from '../router';

export default {
  data() {
    return {
      email: '',
      password: '',
      message: '',
      status: ''
    };
  },
  methods: {
    submitForm() {
      if (this.email && this.password) {
        this.login();
      } else {
        this.message = 'Please enter both email and password.';
        this.status = 'error';
      }
    },
    login() {
      const loginData = {
        username: this.email,
        password: this.password
      };

      api.post('/login', loginData)
        .then(response => {
          this.message = response.data.message;
          this.status = response.data.status;
          if (this.status === 'success') {
            const token = response.data.access_token;
            localStorage.setItem('token', token);
            router.push('/dashboard');
          }
        })
        .catch(error => {
          console.error(error);
          this.message = 'An error occurred.';
          this.status = 'error';
        });

      this.email = '';
      this.password = '';
    },
    register() {
      // Implement registration logic
    }
  }
};
</script>

<style scoped>
.signin-content-section {
  background-image: url("../assets/iitm_main_blur.jpg");
  background-position: 50%;
  background-size: cover;
  flex-flow: column;
  justify-content: center;
  align-items: center;
  height: 84vh;
  margin-top: 10vh;
  margin-bottom: 10vh;
  display: flex;
  position: fixed;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
}

.signin-section {
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
  background-color: rgba(255, 255, 255, .6);
  border-radius: 30px;
  min-width: 400px;
  min-height: 400px;
  margin: 0% 0;
  padding: 0%;
}

.signin-title {
  justify-content: center;
  align-items: center;
  margin-bottom: 5px;
  padding: 16px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-size: 35px;
  font-weight: 300;
  display: flex;
}

.signin-with-google {
  box-sizing: border-box;
  aspect-ratio: auto;
  object-fit: fill;
  background-color: #fff;
  border-radius: 16px;
  justify-content: center;
  align-items: center;
  margin-left: 88px;
  margin-right: 88px;
  padding-top: 6px;
  padding-bottom: 6px;
  display: flex;
  padding-left: 19px;
}

.sign-in-with-google-button {
  color: var(--grey);
  background-color: rgba(56, 152, 236, 0);
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.form-label {
  align-self: flex-start;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-weight: 400;
}

.sign-in-form {
  flex-flow: column;
  justify-content: center;
  align-items: stretch;
  display: flex;
}

.sign-in-form-block {
  aspect-ratio: auto;
  margin-top: 7px;
  margin-bottom: 22px;
  padding-left: 26px;
  padding-right: 26px;
}

.signin-or-option {
  justify-content: center;
  align-items: center;
  margin-top: 10px;
  font-family: Ubuntu, Helvetica, sans-serif;
  display: flex;
}

.signin-button {
  aspect-ratio: auto;
  background-color: var(--iitm-theme-red);
  object-fit: fill;
  border-radius: 20px;
  align-self: center;
  margin-top: 18px;
  padding-left: 27px;
  padding-right: 27px;
  font-family: Ubuntu, Helvetica, sans-serif;
  font-size: 16px;
  font-weight: 500;
  color: #fff;
}

.signin-text {
  border-radius: 13px;
}

.alert {
  border-radius: 4px;
  font-size: 14px;
  padding: 12px 20px;
  margin-top: 20px;
}

.alert-success {
  background-color: #d4edda;
  border-color: #c3e6cb;
  color: #155724;
}

.alert-danger {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}
</style>
