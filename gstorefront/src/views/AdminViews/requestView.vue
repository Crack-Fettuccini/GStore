<template>
    <div>
      <div v-if="dataLoading">
        Getting all requests from users to become admin...
      </div>
      <div v-else class="flex-container">
        <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
          <span>{{ ErrorMessage }}</span>
        </div>
        <div v-if="SuccessMessage" class="alert alert-success fade show error-message" role="alert">
            <span>{{ SuccessMessage }}</span>
        </div>
        <h1 id="title_card" class="display-6">Approval list for Admin access</h1>
        <div class="row justify-content-center">
          <div class="col-xs-12 col-sm-10">
            <table class="table table-striped  text-start">
              <thead>
                <tr>
                  <th class="col-1" scope="col">#</th>
                  <th class="col-8" scope="col">Email</th>
                  <th class="col-3" scope="col">Approve/Reject</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(email,index) in emails" :key="email.email" class="" style="">
                  <th scope="row">{{ index + 1 }}</th>
                  <td>{{ email.email }}</td>
                  <td>
                    <div class="btn-group" role="group">
                      <button type="submit" class="btn btn-success" @click="confirmRequestForAdminState(email.email, 'approve')">Approve</button>
                      <button type="button" class="btn btn-danger" @click="confirmRequestForAdminState(email.email, 'reject')">Reject</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
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
            emails: {},
            dataLoading: true,
            ErrorMessage:null,
            SuccessMessage:null,
          };
        },
        mounted() {
          this.fetchRequestsForAdminState();
        },
        methods: {
          async fetchRequestsForAdminState() {
            try {
              const response = await this.$axios.get('/requestAdminPrivilege');
              this.emails = response.data.msg;
            } catch (error) {
              console.error('Error fetching data:', error);
              if (error.response && error.response.data && error.response.data.msg) {
               this.ErrorMessage = error.response.data.msg;
                this.SuccessMessage = null;
              } else if (error.response && error.response.data && error.response.data.message) {
                this.SuccessMessage = null;
                this.ErrorMessage = error.response.data.msg;
              } else {
                this.SuccessMessage = null;
                this.ErrorMessage = 'An error occurred. Please try again later.';
              }
            } finally {
              this.dataLoading = false;
            }
          },
          confirmRequestForAdminState(email, state) {
            if (state==='reject' || state==="approve"){
              const confirmation = window.confirm(`Are you sure you want to ${state} ${email}'s request to be an admin?`);
              if (confirmation) {
                if (state==='approve'){
                  this.processRequestForAdminState(email, 'true');
                } else if (state==='reject'){
                  this.processRequestForAdminState(email, 'false');
                } 
              }
            }
          },
          async processRequestForAdminState(email, state) {
            try {
              const response = await this.$axios.patch('/requestAdminPrivilege',{
                email:email,
                approval:state,
              });
              this.SuccessMessage = response.data.msg;
              this.ErrorMessage = null
              if (response.status === 200) {
                this.fetchRequestsForAdminState();
                this.SuccessMessage = response.data.msg;
                this.ErrorMessage = null
              }
            } catch (error) {
              console.error('Error fetching data:', error);
              if (error.response && error.response.data && error.response.data.msg) {
               this.ErrorMessage = error.response.data.msg;
                this.SuccessMessage = null;
              } else if (error.response && error.response.data && error.response.data.message) {
                this.SuccessMessage = null;
                this.ErrorMessage = error.response.data.msg;
              } else {
                this.SuccessMessage = null;
                this.ErrorMessage = 'An error occurred. Please try again later.';
              }
            }
          },
        },
      };
      </script>