<template>
  <div class="Login">
    <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
      <span>{{ ErrorMessage }}</span>
    </div>
    <LoginComponent  @form-submitted="submitForm" LogSign="Login"/>
  </div>
</template>

<script>
import LoginComponent from '@/components/LoginComponent.vue'

export default {
  name: 'LoginView',
  components: {
    LoginComponent
  },
  data() {
    return {
      ErrorMessage: null,
    };
  },
  methods: {
    async submitForm({ email, password }) {
      try {
        const response = await this.$axios.post('/login', {
          email: email,
          password: password},{
          withCredentials: true});
        if (response.status === 200) {
          this.$store.dispatch('resetState');
          let accesstoken = response.data.accessToken;
          let userlevel = response.data.userLevel;
          this.$store.commit('setAccessToken', accesstoken);
          this.$store.commit('setUserLevel', userlevel);
          console.log(this.$store.state.access_token)
          if (userlevel==='U'){
            this.$router.push({path:'/user/dashboard'});
          } else if(userlevel==='M') {
            this.$router.push({path:'/manager/dashboard'});
          } else if(userlevel==='A') {
            this.$router.push({path:'/admin/dashboard'});
          }
        }
      } catch (error) {
        console.error('Error:', error);
        if (error.response && error.response.data && error.response.data.msg) {
          this.ErrorMessage = error.response.data.msg;
        } else {
          this.ErrorMessage = 'An error occurred. Please try again later.';
        }
      }
    }
  }
}
</script>
