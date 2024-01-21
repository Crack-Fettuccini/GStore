<template>
  <nav v-if="this.$store.state.userLevel==='U'" class="navbar">
    <div id="dashboard" class="float-start">
      &emsp;
      <router-link to="/user/dashboard">Dashboard</router-link>
    </div>
    <transition name="fade" mode="out-in">
      <div id="searchdiv" style="position: absolute; left: 35%; right: 35%;">
        <input v-if="$route.path === '/user/dashboard'"  v-model="Search" class="form-control" type="text" name="Search" id="rePSearchassword" placeholder="Search">
      </div>
    </transition>
    <div id="userActivity" class="float-end">
      <router-link to="/user/profile">Profile</router-link> |
      <router-link to="/user/orders">Orders</router-link> |
      <router-link @click="logout" to="/login">Logout</router-link>
      &emsp;
    </div>
  </nav>
  <nav v-else-if="this.$store.state.userLevel==='M'" class="navbar">
    <div id="dashboard" class="float-start">
      &emsp;
      <router-link to="/manager/dashboard">Dashboard</router-link>
    </div>
    <transition name="fade" mode="out-in">
      <div id="searchdiv" style="position: absolute; left: 35%; right: 35%;">
        <input v-if="$route.path === '/manager/dashboard'"  v-model="Search" class="form-control" type="text" name="Search" id="rePSearchassword" placeholder="Search">
      </div>
    </transition>
    <div id="userActivity" class="float-end">
      <router-link to="/manager/profile">Profile</router-link> |
      <router-link to="/manager/tickets">Tickets</router-link> |
      <router-link @click="logout" to="/login">Logout</router-link>
      &emsp;
    </div>
  </nav>
  <nav v-if="this.$store.state.userLevel==='A'" class="navbar">
    <div id="dashboard" class="float-start">
      &emsp;
      <router-link to="/admin/dashboard">Dashboard</router-link> |
      <router-link to="/admin/requests">Requests</router-link>
    </div>
    <div id="userActivity" class="float-end">
      <router-link to="/admin/profile">Profile</router-link> |
      <router-link to="/admin/tickets">Tickets</router-link> |
      <router-link @click="logout" to="/login">Logout</router-link>
      &emsp;
    </div>
  </nav>
  <br>
  <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
      <span>{{ ErrorMessage }}</span>
  </div>
  <div v-if="SuccessMessage" class="alert alert-success fade show error-message" role="alert">
      <span>{{ SuccessMessage }}</span>
  </div>
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" :search="Search"/>
    </transition>
  </router-view>
</template>

<style>
div #authentication{
  align-items: end;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s linear;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

</style>

<script>
export default {
  name: 'PrelogView',
  data() {
    return {
      Search: '',
      ErrorMessage:null,
      SuccessMessage:null,
    };
  },
  methods: {
    async logout() {
      try {
        let response = await this.$axios.delete('/logout');
        if (response.status === 200) {
            this.ErrorMessage = null;
            this.SuccessMessage = response.data.msg;
          }
      } catch (error) {
          console.error('Error:', error);
          if (error.response && error.response.data && error.response.data.msg) {
            this.SuccessMessage = null;
            this.ErrorMessage = error.response.data.msg;
          } else if (error.response && error.response.data && error.response.data.message) {
            this.SuccessMessage = null;
            this.ErrorMessage = error.response.data.msg;
          } else {
            this.SuccessMessage = null;
            this.ErrorMessage = 'An error occurred. Please try again later.';
          }
        }
      this.$store.dispatch('resetState');
      this.$router.push('/login');
    },
  },
};

</script>