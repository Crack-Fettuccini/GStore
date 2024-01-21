<template>
  <div>
    <div v-if="dataLoading">
      Getting all request tickets...
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
            <div v-for="(ticket,index) in tickets" :key="ticket.requestID" class="accordion-item" :class="ticket.status">
              <h2 class="accordion-header">
                <button class="accordion-button" type="button" data-bs-toggle="collapse" :data-bs-target="'#ticketbody'+index">
                  {{ticket.requestTitle}}
                </button>
              </h2>
              <div :id="'ticketbody' + index" class="accordion-collapse collapse" data-bs-parent="#ticketAccordion">
                <div class="accordion-body">
                  <div>
                    {{ticket.requestMessage}}
                  </div>
                  <div class="form-floating" style="overflow: auto;">
                    <textarea class="form-control" placeholder="Ticket Body" id="ticketBody" v-model="adminMessage[ticket.requestID]"></textarea>
                    <label for="ticketBody">Reason for approval/rejection</label>
                    <button style="margin-top: 15px;" type="button" class="btn btn-danger float-start" @click="confirmProcessTicket(ticket, 'reject')" :disabled="adminMessage[ticket.requestID]===''">Reject</button>
                    <button style="margin-top: 15px;" type="button" class="btn btn-success float-end" @click="confirmProcessTicket(ticket, 'approve')" :disabled="adminMessage[ticket.requestID]===''">Approve</button>
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
          adminMessage:{},
          ErrorMessage:null,
          SuccessMessage:null,
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
            this.tickets.forEach(ticket => {
              this.adminMessage[ticket.requestID] = '';
            });
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
        confirmProcessTicket(ticket, state) {
          if (state==='reject' || state==="approve"){
            const confirmation = window.confirm(`Are you sure you want to ${state} request '${ticket.requestTitle}'?`);
            if (confirmation) {
              if (state==='reject'){
                this.processTicket(ticket.requestID, 'Rejected');
              } else if (state==='approve'){
                this.processTicket(ticket.requestID, 'Approved');
              }
            }
          }
        },
        async processTicket(requestID, state) {
          try {
            const response = await this.$axios.patch('/tickets',{
              requestID:requestID,
              Resolution:state,
              AdminMessage:this.adminMessage[requestID]
            });
            this.SuccessMessage = response.data.msg;
            this.ErrorMessage = null
            if (response.status === 200) {
              this.fetchTickets();
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