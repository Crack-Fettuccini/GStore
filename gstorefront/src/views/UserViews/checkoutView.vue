<template>
  <div>
    <div v-if="dataLoading">
      Loading...
    </div>
    <div v-else-if="allowPurchase" class="flex-container">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10">
          <router-link to="/user/dashboard" class="float-start">&lt;&nbsp;Back</router-link>
          <h1 id="title_card" class="display-6">Checkout</h1>
          <table class="table table-striped  text-start">
            <thead>
              <tr>
                <th class="col-1" scope="col">#</th>
                <th class="col-5" scope="col">Item</th>
                <th class="col-2" scope="col">Qty</th>
                <th class="col-1" scope="col">Price</th>
                <th class="col-1" scope="col">Remove</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(qty, productId, index) in selections" :key="productId" class="" style="">
                <th scope="row">{{ index + 1 }}</th>
                <td>{{ productName(productId) }}</td>
                <td>{{qty}}</td>
                <td>&#8377;{{ calculatePrice(productId, qty) }}</td>
                <td>
                  <button type="button" class="btn btn-danger"  @click="removeItem(productId)">&#x1F5D1;</button>
                </td>
              </tr>
            </tbody>
            <tfoot>
              <th scope="row"></th>
              <td></td>
              <td style="background-color: white;">Total:</td>
              <td class="fw-semibold" style="background-color: white;">&#8377;{{ calculateTotalCost() }}&nbsp;</td>
              <td style="background-color: white;"></td>
            </tfoot>
          </table>
          <div class="float-end" style="transform: translate(0%, 75%);">
            <button type="button" class="btn btn-success text-center" @click="purchaseItems(selections)">&#x1F6D2; Checkout</button>
            <span>&nbsp;</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div> No items in cart</div>
    </div>
  </div>
</template>

<style>
.fade-in {
  opacity: 0;
  transform: translateY(100%);
  transition: opacity 50ms ease-in, transform 100ms ease-out;
}
.fade-in.visible {
  transform: translateY(0);
  opacity: 1;
}
</style>

<script>
import { mapMutations, mapGetters } from 'vuex';

export default {
  name: 'itemsView',
  data() {
    return {
      apiData: [],
      dataLoading: true,
      selectedQuantities: {},
    };
  },
  computed: {
    ...mapGetters(['getWrittenQuantities']),
    allowPurchase() {
      return Object.values(this.selectedQuantities).some(quantity => quantity > 0);
    },
    selections() {
      return Object.fromEntries(Object.entries(this.selectedQuantities).filter((keyval) => keyval[1] !== 0));
    }
  },
  mounted() {
    this.fetchCart();
  },
  methods: {
    ...mapMutations(['updateWrittenQuantities']), // Map the mutation to use in methods
    async fetchCart() {
      try {
        const response = await this.$axios.get('/modifyProducts');
        this.apiData = response.data.msg;
        const writtenQuantities = this.getWrittenQuantities;
        if (writtenQuantities && Object.keys(writtenQuantities).length > 0) {
          this.selectedQuantities = writtenQuantities;
        } else {
          this.apiData.forEach(item => {
            this.selectedQuantities[item.productID] = 0;
          });
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        this.dataLoading = false;
      }
    },
    calculatePrice(productId, quantity) {
      const product = this.apiData.find(item => item.productID === parseInt(productId));
      if (quantity === undefined || product === undefined) {
        return '0';
      }
      return parseFloat((quantity * product.pricePerUnit).toFixed(2));
    },
    productName(productId){
      const product = this.apiData.find(item => item.productID === parseInt(productId));
      return product.productName
    },
    calculateTotalCost() {
        return Object.entries(this.$store.state.writtenQuantities).reduce((total, [productId,quantity]) => {
          const product = this.apiData.find(item => item.productID === parseInt(productId));
          return parseFloat(total + parseFloat((quantity * product.pricePerUnit).toFixed(2)));
        }, 0);
      },
    removeItem(productId) {
      this.selectedQuantities[productId]=0;
    },
    async purchaseItems(selections) {
      try {
        const response = await this.$axios.post('/purchases', {
          purchaseList: selections},
          {withCredentials: true});
        if (response.status === 200) {
          this.$store.commit('updateWrittenQuantities',{});
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
  },
};
</script>
  