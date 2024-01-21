<template>
  <div>
    <!-- Your component content here -->
    <div v-if="dataLoading">
      Loading...
    </div>
    <div v-else class="flex-container">
      <div v-if="successMessage" class="alert alert-success" role="alert">
        <span>{{ successMessage }}</span>
      </div>
      <div v-if="ErrorMessage" class="alert alert-danger" role="alert">
        <span>{{ ErrorMessage }}</span>
      </div>
      <div class="row justify-content-md-center">
        <div class="col col-lg-4 col-md-6 col-sm-10">
          <div id="editings container" style="position:static;">
            <form @submit.prevent="changeUsername">
              <label for="username" class="col-form-label fw-semibold">Change Username</label>
              <div class="input-group">
                <input type="string" class="form-control" name="username" id="username" placeholder="Username" v-model="username" required>
                <button type="submit" class="btn btn-primary float-end" value="Submit">Change Username</button>
              </div>
            </form>
            <div>
              <form @submit.prevent="changeEmail">
                <label for="Email" class="col-form-label fw-semibold">New Email address</label>
                <div class="input-group">
                  <input type="email" class="form-control" name="Email" id="Email" placeholder="name@example.com" v-model="email" required>
                  <button type="submit" class="btn btn-primary float-end" id="button-addon2" value="Submit">Change Email</button>
                </div>
                <small>
                  <span id="email guide">Enter a </span>
                  <span :style="{ color: (emailValid ? 'green' : 'red')}" id="Ema">valid email</span>
                </small>
              </form>
            </div>
            <form  @submit.prevent="changePassword">
              <div class="row g-3">
                <div class="col md-6">
                  <label for="Password" class="col-form-label fw-semibold">Current password</label>
                  <input :type="(showPassword ? 'text' : 'password')" class="form-control" name="Password" id="Password" v-model="password" placeholder="Current Password">
                </div>
                <div class="col md-6">
                  <label for="NewPassword" class="col-form-label fw-semibold">New password</label>
                  <input :type="(showPassword ? 'text' : 'password')" class="form-control" name="NewPassword" id="NewPassword" v-model="repassword" 
                  placeholder="Password1" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" required>
                </div>
                <small>
                  <div id="password_guide">
                    <span>New password requires atleast&nbsp;</span>
                    <span :style="{ color: (uppercase ? 'green' : 'red')}">1 Uppercase,</span>
                    <span :style="{ color: (lowercase ? 'green' : 'red')}"> 1 lowercase,</span>
                    <span :style="{ color: (number ? 'green' : 'red')}"> 1 number,</span>
                    <span :style="{ color: (length ? 'green' : 'red')}">and atleast 8 characters.</span>
                  </div>
                </small>
              </div>
              <div>
                <input type="checkbox" v-model="showPassword" class="form-check-input" id="VisibilityToggle" style="padding-top: 5px;">
                <label class="form-check-label" for="VisibilityToggle">View Password</label>
              </div>
              <div style="position: relative; right:0%;">
                <button type="submit" class="btn btn-primary" value="Submit">Change Password</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'itemsView',
  data() {
    return {
      showPassword: false,
      email: null,
      username: null,
      password: "",
      repassword: "",
      dataLoading: true,
      successMessage: null,
      ErrorMessage: null,
      emailValid: true,
      lowercase: true,
      uppercase: true,
      number: true,
      length: true,
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    toggleVisibility() {
      this.showPassword = !this.showPassword;
    },
    validateEmail() {
      this.emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email);
    },
    validatePassword() {
      this.lowercase = /[a-z]/.test(this.password);
      this.uppercase = /[A-Z]/.test(this.password);
      this.number = /[0-9]/.test(this.password);
      this.length = this.password.length > 7;
    },
    async fetchProfile() {
      try {
        const response = await this.$axios.get('/editProfile');
        this.username = response.data.username;
        this.email = response.data.email;
      } catch (error) {
        console.error('Error fetching profile data:', error);
      } finally {
        this.dataLoading = false;
      }
    },
    async changeUsername() {
      try {
        const response = await this.$axios.patch('/editProfile',{
          username: this.username},{
          withCredentials: true});
        if (response.status === 200) {
          this.successMessage = response.data.msg;
          this.ErrorMessage = null;
        }
      } catch (error) {
        console.error('Error:', error);
        if (error.response.data.msg) {
          this.ErrorMessage = error.response.data.msg;
          this.successMessage = null;
        } else {
          this.ErrorMessage = 'An error occurred. Please try again later.';
        }
      }    
    },
    async changeEmail() {
      try {
        const response = await this.$axios.patch('/editProfile',{
          email: this.email},{
          withCredentials: true});
        if (response.status === 200) {
          this.successMessage = response.data.msg;
          this.ErrorMessage = null;
        }
      } catch (error) {
        console.error('Error:', error);
        if (error.response.data.msg) {
          this.ErrorMessage = error.response.data.msg;
          this.successMessage = null;
        } else {
          this.ErrorMessage = 'An error occurred. Please try again later.';
        }
      }
    },
    async changePassword() {
      try {
        const response = await this.$axios.patch('/editProfile',{
          currentPassword: this.password,
          newPassword: this.repassword,
        },{
          withCredentials: true});
        if (response.status === 200) {
          this.successMessage = response.data.msg;
          this.ErrorMessage = null;
        }
      } catch (error) {
        console.error('Error:', error);
        if (error.response.data.msg) {
          this.ErrorMessage = error.response.data.msg;
          this.successMessage = null;
        } else {
          this.ErrorMessage = 'An error occurred. Please try again later.';
        }
      }
    },
  },
};
</script>
  