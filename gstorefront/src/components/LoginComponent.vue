<template>
  <br>
  <br>
  <div class="login">
    <div class="card mx-auto" style="width: 20rem !important; align-items: center;">
      <div class="card-body">
        <h4 class="card-title">{{LogSign}}</h4>
        <form @submit.prevent="submitForm">
          <div class="collapse show" id="login">
            <div>
              <label for="Email" class="col-form-label">Email address</label>
              <input v-model="email" style="text-align: left" type="email" class="form-control" @input="validateEmail" name="Email" id="Email" placeholder="name@example.com" required>
              <small class="float-start">
                <div id="email_guide">
                  Enter a
                  <span id="Ema" :style="{ color: (emailValid ? 'green' : 'red')}">valid email</span>
                </div>
              </small>
            </div>
            <br>
            <div>
              <label for="Password" class="col-form-label">Password</label>
              <input v-model="password" :type="(showPassword ? 'text' : 'password')" class="form-control" name="Password" @input="validatePassword" id="Password" 
                placeholder="Password1" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" required>
              <small class="float-start" style="text-align: left;">
                <div id="password_guide">
                  Password requires 
                  <span id="ucase"  :style="{ color: (lowercase ? 'green' : 'red')}">1 Uppercase,</span>
                  <span id="lcase" :style="{ color: (uppercase ? 'green' : 'red')}"> 1 lowercase,</span>
                  <span id="num"  :style="{ color: (number ? 'green' : 'red')}"> 1 number,</span>
                  <span id="length" :style="{ color: (length ? 'green' : 'red')}">and atleast 8 characters.</span>
                </div>
              </small>
            </div>
            <slot name="doublecheck" :showPass="showPassword" :password="password">
            </slot>
            <br>
            <br>
            <div>
              <input type="checkbox" v-model="showPassword" class="form-check-input float-start" id="VisibilityToggle" style="padding-top: 5px;">
              <label class="form-check-label float-start" for="VisibilityToggle">View Password</label>
            </div>
            <br>
            <br>
            <div class="d-grid gap-2">
              <input type="submit" class="btn btn-primary" :value="LogSign" :disabled="!emailValid || !lowercase || !uppercase || !number || !length">
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'LoginComponent',
    emits: ['form-submitted','toggle-visibility'],
    props: {
      LogSign: String,
    },
  data() {
    return {
      showPassword: false,
      email: '',
      emailValid: false,
      password: '',
      lowercase: false,
      uppercase: false,
      number: false,
      length: false,
    };
  },
  methods: {
    submitForm() {
      this.$emit('form-submitted', { email: this.email, password: this.password });
    },
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
    }
  },
};
</script>
