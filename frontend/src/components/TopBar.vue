<template>
  <div class="top-bar">
    <div class="container">
      <!-- Any additional elements for the left side of the top bar can go here -->
      <div class="spacer"></div>
      
      <!-- User Profile with Dropdown -->
      <div class="user-profile" @click="toggleDropdown">
        <img src="https://www.w3schools.com/howto/img_avatar.png" alt="User Avatar" class="avatar">
        <!-- Dropdown Menu -->
        <ul v-if="showDropdown" class="dropdown-menu">
          <li><a href="#">Profile</a></li>
          <li><a href="#">Settings</a></li>
          <li><a href="#" @click="logout">Logout</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDropdown: false
    };
  },
  methods: {
    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    },
    
   



    logout() {
         // Clear the data from localStorage
      localStorage.removeItem('token');


      // Redirect to the login page
      this.$router.push('/');
   
 

    }
  }
};
</script>

<style scoped>
.top-bar {
  background-color: #007bff;
  color: #fff;
  height: 50px;
  display: flex;
  align-items: center;
}

.container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.spacer {
  flex: 1;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer; /* Change cursor to pointer on hover */
  position: relative; /* Position relative for absolute positioning of dropdown */
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.dropdown-menu {
  position: absolute;
  top: 55px; /* Adjust dropdown position below avatar */
  right: 0;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  list-style: none;
  padding: 8px 0;
  min-width: 120px;
  z-index: 1000;
}

.dropdown-menu li {
  padding: 8px 20px;
}

.dropdown-menu li a {
  color: #333;
  text-decoration: none;
  display: block;
  transition: background-color 0.3s;
}

.dropdown-menu li a:hover {
  background-color: #f0f0f0;
}
</style>
