<template>
  <div class="Register">
    <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
      <span>{{ ErrorMessage }}</span>
    </div>
    <LoginComponent  @form-submitted="submitForm" LogSign="Register">
      <template v-slot:doublecheck="slotProps">
        <div>
          <label for="ExtraInput" class="col-form-label">Re-enter Password</label>
          <input v-model="rePassword" :type="(slotProps.showPass ? 'text' : 'password')" class="form-control" name="rePassword" id="rePassword" placeholder="Password1" required>
          <small class="float-start">
            <div id="repassword_guide">
              <span id="repass" :style="{ color: (this.rePassword.length < 8 ? 'black' : (slotProps.password === rePassword ? 'green' : 'red'))}">valid email</span>
            </div>
          </small>
        </div>
      </template>
    </LoginComponent>
  </div>
</template>

<script>
import LoginComponent from '@/components/LoginComponent.vue'

export default {
  name: 'RegistrationView',
  components: {
    LoginComponent
  },
  data() {
    return {
      rePassword: '',
      passwordMatch: false,
      ErrorMessage: null,
//      showPassword: false,
    };
  },
  methods: {
    inputType() {
      return this.showPassword ? 'text' : 'password';
    },
    async submitForm({ email, password }) {
      try {
        const response = await this.$axios.post('/register', {
          email: email,
          password: password,
          passwordCheck: this.rePassword
        });
        if (response.status === 200) {
          let accesstoken = response.data.access_token;
          this.$store.commit('setAccessToken', accesstoken);
          console.log(this.$store.state.access_token)
          this.$router.push({path:'/user/dashboard'});
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
