<template>
  <div>
    <div v-if="dataLoading">
      Getting your tickets...
    </div>
    <div v-else class="flex-container">
      <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
        <span>{{ ErrorMessage }}</span>
      </div>
      <div v-if="SuccessMessage" class="alert alert-success fade show error-message" role="alert">
          <span>{{ SuccessMessage }}</span>
      </div>
      <h1 id="title_card" class="display-6">Tickets</h1>      
      <div class="row justify-content-center">
        <div class="col-xs-12 col-sm-10">
          <div class="accordion" id="ticketAccordion">
            <div  class="accordion-item" style="border-color:#42b98377 !important;">
              <h2 class="accordion-header">
                <button class="accordion-button" style="background-color:#42b983;" type="button" data-bs-toggle="collapse" data-bs-target="#newTicket">
                  New Ticket
                </button>
              </h2>
              <div id="newTicket" class="accordion-collapse collapse show" data-bs-parent="#ticketAccordion" style="background-color:#42b98377;">
                <div class="accordion-body">
                  <form @submit.prevent="createTicket()" style="overflow: auto;">
                    <div class="input-group" :class="selectedAction" style="display: flex; align-items: center;">
                      <select v-model="selectedAction" id="actionSelect" class="form-select">
                        <option value="" disabled selected>Select an action</option>
                        <option value="create">Create</option>
                        <option value="rename">Rename</option>
                        <option value="delete">Delete</option>
                      </select>
                
                      <template v-if="selectedAction === 'create'">
                        <span class="input-group-text"> new category with name </span>
                        <input type="text" v-model="ticketTitle1" class="form-control" placeholder="name of new category">
                      </template>

                      <template v-else-if="selectedAction === 'rename'">
                        <select ref="changecat" id="category" name="category" v-model="ticketTitle1" class="form-select">
                          <option value="" disabled selected>Select category </option>
                          <option v-for="cat in categories" :key="cat" :value=cat>{{cat}}</option>
                        </select>
                        <span class="input-group-text"> as </span>
                        <input type="text" v-model="ticketTitle2" class="form-control" placeholder="Enter new name">
                      </template>

                      <template v-else-if="selectedAction === 'delete'">
                        <select ref="changecat" id="category" name="category" v-model="ticketTitle1" class="form-select">
                          <option value="" disabled selected>Select category </option>
                          <option v-for="cat in categories" :key="cat" :value=cat>{{cat}}</option>
                        </select>
                        <span class="input-group-text"> and move products to </span>
                        <select ref="changecat" id="category" name="category" v-model="ticketTitle2" class="form-select">
                          <option value="" disabled selected>Select category </option>
                          <option v-for="cat in filteredCategories(ticketTitle1)" :key="cat" :value=cat>{{cat}}</option>
                        </select>
                      </template>
                    </div>
                    <div class="form-floating" style="overflow: auto;">
                      <textarea style="height:100px" class="form-control" placeholder="Ticket Body" id="ticketBody" v-model="ticketBody"></textarea>
                      <label for="ticketBody">Reason for request</label>
                    </div>
                    <button style="margin-top: 15px;" type="submit" class="btn btn-success float-end" :disabled="ticketTitle1==='' || ticketBody===''">Send Request</button>
                  </form>
                </div>
              </div>
            </div>
            <div v-for="(ticket,index) in tickets" :key="ticket.requestID" class="accordion-item" :class="ticket.status">
              <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#ticketbody'+index">
                  {{ticket.requestTitle}}
                </button>
              </h2>
              <div :id="'ticketbody' + index" class="accordion-collapse collapse" data-bs-parent="#ticketAccordion">
                <div class="accordion-body">
                  <div>Explanation:</div>
                  <div>
                    {{ticket.requestMessage}}
                  </div>
                  <div v-if="ticket.status==='Approved'">Admin reply:</div>
                  <div v-else-if="ticket.status==='Rejected'">Reason for rejection:</div>
                  <div v-if="ticket.status==='Approved' || ticket.status==='Rejected'">
                    {{ticket.adminMessge}}
                  </div>
                  <div style="overflow: auto;">
                    <button type="button" class="btn btn-danger float-end" @click="confirmDeleteTicket(ticket)">Delete Request</button>
                  </div>
                </div>
              </div>
            </div>
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
        tickets: {},
        dataLoading: true,
        selectedAction: '',
        ticketTitle1:'',
        ticketTitle2:'',
        ticketBody:'',
        ErrorMessage:null,
        SuccessMessage:null,
        categories: [],
      };
    },
    mounted() {
      this.fetchTickets();
    },
    methods: {
      async fetchTickets() {
        try {
          const response = await this.$axios.get('/tickets');
          this.tickets = response.data.msg;
          const resp = await this.$axios.get('/modifyCategory');
          this.categories = resp.data.msg;

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

      async createTicket() {
        try {
          let ticketTitle = "";
          if(this.selectedAction==='create'){
            ticketTitle = `Create category ${this.ticketTitle1}`;
          } else if (this.selectedAction==='rename'){
            ticketTitle = `Rename category ${this.ticketTitle1} to ${this.ticketTitle2}`;
          } else if (this.selectedAction==='delete'){
            ticketTitle = `Delete category ${this.ticketTitle1} and move products to ${this.ticketTitle2}`;
          }
          const response = await this.$axios.post('/tickets',{
            title:ticketTitle,
            request:this.ticketBody
          });
          this.SuccessMessage = response.data.msg;
          this.ErrorMessage = null
          if (response.status === 200) {
            this.fetchTickets();
            this.ticketTitle1 = '';
            this.ticketTitle2 = '';
            this.ticketBody = '';
            this.SuccessMessage = response.data.msg;
            this.ErrorMessage = null
            this.fetchTickets();
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
      confirmDeleteTicket(ticket) {
      const confirmation = window.confirm(`Are you sure you want to delete request '${ticket.requestTitle}'?`);
      if (confirmation) {
        this.deleteTicket(ticket.requestID);
      }
    },
      async deleteTicket(requestID) {
        try {
          const response = await this.$axios.delete(`/tickets/${requestID}`,
            {withCredentials: true});
          if (response.status === 200) {
            this.fetchTickets();
            this.SuccessMessage = response.data.msg;
            this.ErrorMessage = null
          }
        } catch (error) {
          console.error('Error:', error);
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
      filteredCategories(currentCategory) {
        return this.categories.filter((cat) => cat !== currentCategory);
      },
    },
    watch: {
    selectedAction() {
      this.ticketTitle1 = '';
      this.ticketTitle2 = '';
    },
  },
  };
</script>
<style>
  .input-group-text{
    color:white;
  }
  .input-group.create .input-group-text{
    background-color: #198754;
  }

  .input-group.rename  .input-group-text{
    background-color: #ffc107;
  }

  .input-group.delete  .input-group-text{
    background-color: #dc3545;
  }
</style>