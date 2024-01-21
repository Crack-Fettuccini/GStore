<template>
  <div>
    <div v-if="dataLoading">
      Loading...
    </div>
    <div v-else class="flex-container">
      <h1 id="title_card" class="display-5">Products</h1>
      <div class="input-group" role="group">
        <label class="input-group-text" for="quantity" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);">Min Price:&nbsp;</label>
        <input v-model="minPPU" type="number" min="0" step=".01" class="form-control">
        <label class="input-group-text" for="quantity" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);">Max Price:&nbsp;</label>
        <input v-model="maxPPU" type="number" max="9999" step=".01" class="form-control">
        <button :key="'all'" class="btn btn-success" @click="resetPriceFilter()">Reset Price Filter</button>
      </div>
      <br>
      <div class="btn-group" role="group">
        <button :key="'all'" class="btn" :class="'all' === selectedCategory ? 'btn-success' : 'btn-secondary'" @click="changeCategory('all')">
          All
        </button>
        <button v-for="category in categories" :key="category" class="btn" :class="category === selectedCategory ? 'btn-success' : 'btn-secondary'" @click="changeCategory(category)">
          {{ category }}
        </button>
      </div>
      <br>
      <br>
      <div class="flex-row justify-content-evenly  d-flex flex-wrap">
        <div v-for="(item, index) in filteredData" :key="item.productID" class=" justify-content-evenly d-flex flex-wrap c-container col-sm-12 col-md-6 col-lg-3 col-xl-3" :style="{'animation-delay': index*50+'ms'}">
          <div class="card align-self-center" :class="{'outofstock': item.availableStock === 0 }">
            <div class="front">
              <img :src=item.productImage class="card-img-top" alt="..." style="position:relative; object-fit: cover; width: 100%; height: 50%; border-top-right-radius: 5%;border-top-left-radius: 5%;">
              <div v-if="item.availableStock===0" style="position:absolute; top:0; width:100%; height:100%; font-size: xx-large; font-weight:500;backdrop-filter: blur(2px); z-index: 5; background-color: #adb5bd77;">
                <br>
                <br>
                Sold Out
              </div>
              <div class="card-body" style=" text-align: center;">
                <h3 class="card-title">{{ item.productName }}</h3>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Stock:&nbsp;</span>
                  <span style="position: absolute; left:45%">{{item.availableStock-selectedQuantities[item.productID]}}{{item.Unit}}</span>
                </div>
                <br>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Price:&nbsp;</span>
                  <span style="position: absolute; left:45%">&#8377;{{item.pricePerUnit}}/{{item.Unit}}</span>
                </div>
              </div>
            </div>
            <div class="back" v-if="item.availableStock>0">
              <br>
              <div class="card-body" style="padding-top:0; margin-top: 0;">
                <h5 style="margin: -5%;white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">Buy {{item.productName}}</h5>
                <br>
                <br>
                <label for="quantity">Quantity:&nbsp;</label>
                <input v-model="selectedQuantities[item.productID]" type="number" id="quantity" name="quantity" min="0" :max=item.availableStock class="form-control" style="width:90%">
                <br>
                <br>
                <br>
                <div>
                  <span class="fw-semibold">Price:&nbsp;</span>
                  <span>&#8377;{{item.pricePerUnit}}/{{item.Unit}}</span>
                </div>
                <div>
                  <span class="fw-semibold">
                    Total:&nbsp;
                  </span>
                  <span>
                    &#8377;{{ calculatePrice(item.pricePerUnit, selectedQuantities[item.productID]) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div :class="(showCheckout)?'visible fade-in':'fade-in'"  class="sticky-bottom">
        <div v-if="showCheckout" style="height: 12.5vh; box-shadow: inset 0px 1px #ccc; background:#ffffff;">
          <div class="float-end" style="transform: translate(0%, 75%);">
            <span>Total:&nbsp;</span>
            <span class="fw-semibold">&#8377;{{ calculateTotalCost() }}&nbsp;</span>
            <router-link to="/user/checkout">
              <button type="button" class="btn btn-success text-center">&#x1F6D2; Checkout</button>
            </router-link>
            <span>&nbsp;</span>
          </div>
        </div>
      </div>
      <button v-if="this.$store.state.userLevel==='U' && $route.path === '/user/dashboard'" type="button" class="btn btn-light" style="position:absolute; bottom: 0%; left:0%; z-index=-10; " @click="confirmRoleChangeRequest()">Request Manager Role</button>
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
    props: {
      search: String,
    },
    data() {
      return {
        selectedCategory: 'all',
        apiData: [],
        dataLoading: true,
        selectedQuantities: {},
        polling: "",
        minPPU:0,
        maxPPU:9999
      };
    },
    mounted() {
      this.fetchData();
      this.polling = setInterval(this.fetchData, 10000); 
    },
    computed: {
      ...mapGetters(['getWrittenQuantities']), // Map the getter to use in computed
      showCheckout() {
        this.$store.commit('updateWrittenQuantities',this.selectedQuantities);
        console.log('writing', this.getWrittenQuantities)

        return Object.values(this.selectedQuantities).some(quantity => quantity > 0);
      },
      categories() {
        const uniqueCategories = new Set(this.apiData.map(item => item.category));
        return Array.from(uniqueCategories);
      },
      filteredData() {
        let filtered = this.apiData
        const searchlower = this.search.toLowerCase();
        filtered = filtered.filter(item => item.productName.toLowerCase().includes(searchlower));
        if (this.minPPU>0){
          filtered = filtered.filter(item => {
            const productPrice = parseFloat(item.pricePerUnit);
            return productPrice >= this.minPPU;
          });
        }
        if (this.maxPPU<9999){
          filtered = filtered.filter(item => {
            const productPrice = parseFloat(item.pricePerUnit);
            return productPrice <= this.maxPPU;
          });
        }
        if (this.selectedCategory === 'all') {
          return filtered;
        } else {
          return filtered.filter(item => item.category === this.selectedCategory);
        }
      },

    },
    beforeUnmount () {
      clearInterval(this.polling);
    },
    methods: {
      resetPriceFilter(){
        this.minPPU=0;
        this.maxPPU=9999;
      },
      changeCategory(category) {
        this.selectedCategory = category;
      },
      ...mapMutations(['updateWrittenQuantities']), // Map the mutation to use in methods
      async fetchData() {
        try {
          const response = await this.$axios.get('/modifyProducts');
          this.apiData = response.data.msg;
          const writtenQuantities = this.getWrittenQuantities;
          if (writtenQuantities && Object.keys(writtenQuantities).length > 0) {
            this.selectedQuantities = writtenQuantities;
          }
          this.apiData.forEach(item => {
            if (Object.hasOwn(this.selectedQuantities, item.productID)){
              this.selectedQuantities[item.productID] = Math.min(this.selectedQuantities[item.productID], item.availableStock)
            } else{
              this.selectedQuantities[item.productID] = 0;
            }
            this.$store.commit('updateWrittenQuantities',this.selectedQuantities);
          });
          console.log(this.selectedQuantities, "final print")          
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.dataLoading = false;
        }
      },
      calculatePrice(pricePerUnit, quantity) {
        if (quantity === undefined) {
          return '0';
        }
        return parseFloat((pricePerUnit * quantity).toFixed(2));
      },
      calculateTotalCost() {
        return Object.entries(this.$store.state.writtenQuantities).reduce((total, [productId,quantity]) => {
          const product = this.apiData.find(item => item.productID === parseInt(productId));
          return parseFloat(total + parseFloat((quantity * product.pricePerUnit).toFixed(2)));
        }, 0);
      },
      confirmRoleChangeRequest() {
        const confirmation = window.confirm('Are you sure you want to change your role to Store manager?\n You will not be able to purchase any products if request is approved.');
        if (confirmation) {
          this.RequestRoleChange();
        }
      },
      async RequestRoleChange(){
        try {
          const response = await this.$axios.post('/requestAdminPrivilege',{withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = null;
            this.SuccessMessage = response.data.msg;
            this.newItem={productName:"", productImage:"", availableStock:0, pricePerUnit:0, Unit:"g", category:"",}
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
      },
    },
  };
</script>
  