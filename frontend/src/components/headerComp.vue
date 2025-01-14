<template>
    <section class="header-section">
        <div class="logo"><img
                src="../assets/IITMOD-Logo.svg"
                loading="lazy" width="150" alt="" /></div>       
        <router-link :to="`/dashboard`" class="link">
            <div class="title">Student Dashboard</div>
        </router-link>
        <template v-if="$route.name === 'UserLogin'">
            <!-- Custom header content for UserLogin route -->
            <div>
                <a href="#" target="_blank" class="link">Go to Home</a>
                <img
                    src="../assets/icons8-new-tab.svg"
                    loading="lazy" width="25" height="25" alt="" class="open-another-tab-icon" />
            </div>
        </template>
        <template v-else>
            <!-- Custom header content for other routes -->
            <div class="header-user-icon"  @click="toggleDropdown">
                <img
                src="../assets/icons8-user-96.png"
                loading="lazy" width="48" alt="" class="user-avatar" />
                <div class="user-icon-container">
                    <ul v-if="showDropdown" role="list" class="user-icon-dropdown w-list-unstyled">
                        <li class="user-icon-dropdown-item">Profile</li>
                        <li class="user-icon-dropdown-item">Settings</li>
                        <li class="user-icon-dropdown-item" @click="logout">Logout</li>
                    </ul>
                </div>
            </div>
        </template>
    </section>
</template>

<script>
    export default {
        name: 'headerComp',
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
    }
</script>

<style scoped>
.header-section {
    z-index: 100;
    background-color: #fff;
    border-bottom: 3px solid #8d8d8d;
    justify-content: space-between;
    align-items: center;
    height: 10vh;
    margin-bottom: 0;
    padding: 13px;
    display: flex;
    position: fixed;
    top: 0%;
    bottom: auto;
    left: 0%;
    right: 0%;
    box-shadow: 0 7px 12px 3px rgba(0, 0, 0, .33);
  }
.logo {
    justify-content: center;
    align-self: center;
    align-items: center;
    padding-left: 20px;
    display: flex;
}

.header-user-icon {
    flex-flow: column;
    align-self: flex-start;
    align-items: center;
    margin-left: 0;
    padding-top: 9px;
    padding-left: 0;
    padding-right: 0;
    display: flex;
    cursor: pointer;
}

.user-avatar{
    margin-right: 20px;
}

.user-icon-container{
    z-index: 1000;
    float: none;
    justify-content: flex-start;
    align-items: center;
    display: flex;
    position: absolute;
    top: 2px;
    right: 30px;
}

.user-icon-dropdown-item{
    padding: 8px 14px 8px 6px;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-size: 15px;
    cursor: pointer;
    
}

.user-icon-dropdown{
    background-color: var(--red-low-opacity);
    -webkit-backdrop-filter: blur(4px);
    backdrop-filter: blur(4px);
    color: #fff;
    border: 1px solid #acacac;
    border-radius: 9px;
    flex-flow: column;
    align-items: flex-start;
    padding: 11px 18px 11px 11px;
    font-weight: 400;
    display: flex;
    margin-top: 70px;
    box-shadow: 7px 5px 5px rgba(0, 0, 0, .2);
}

.title {
    color: var(--grey);
    text-align: center;
    flex-flow: column;
    justify-content: center;
    align-items: center;
    padding-right: 0;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-size: 31px;
    font-weight: 300;
    display: block;
    cursor: pointer;
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
.link {
    color: var(--iitm-theme-red);
    cursor: pointer;
    font-family: Ubuntu, Helvetica, sans-serif;
    font-size: 18px;
    text-decoration: none;
}
.open-another-tab-icon {
    margin-top: -4px;
}
</style>