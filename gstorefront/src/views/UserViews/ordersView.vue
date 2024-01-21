<template>
  <div>
    <!-- Your component content here -->
    <div v-if="dataLoading">
      Loading...
    </div>
    <div v-else class="flex-container">
      <h1 id="title_card" class="display-6">Order History</h1>
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10">
          <table class="table table-striped  text-start">
            <thead>
              <tr>
                <th class="col-1" scope="col">#</th>
                <th class="col-5" scope="col">Sale ID</th>
                <th class="col-2" scope="col">Date</th>
                <th class="col-1" scope="col">Total</th>
                <th class="col-1" scope="col">Cancel</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(order,index) in purchases" :key="order.SaleID" class="" style="">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ order.saleID }}</td>
                <td>{{order.saleDate}}</td>
                <td>&#8377;{{ order.totalAmount }}</td>
                <td>
                  <button v-if="deleteable(order.saleDate)" class="btn btn-danger" @click="deleteOrder(order.saleID, index)">Delete</button>
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
        purchases: [],
        dataLoading: true,
      };
    },
    mounted() {
      this.fetchPurchases();
    },
    methods: {
      deleteable(saleDated) {
        const saleDate = new Date(saleDated);
      const currentDate = new Date();
      const oneday = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

      return currentDate - saleDate <= oneday;
    },
      async fetchPurchases() {
        try {
          const response = await this.$axios.get('/purchases');
          this.purchases = response.data.msg;
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.dataLoading = false;
        }
      },
      async deleteOrder(saleID,index) {
        try {
          const response = await this.$axios.delete(`/purchases/${saleID}`,
            {withCredentials: true});
          if (response.status === 200) {
            this.purchases.splice(index, 1);
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
    },
  };
  </script>
    