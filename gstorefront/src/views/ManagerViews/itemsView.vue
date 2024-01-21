<template>
  <div>
    <div v-if="dataLoading">
      Loading...
    </div>
    <div v-else class="flex-container">
      <div v-if="ErrorMessage" class="alert alert-danger fade show error-message" role="alert">
          <span>{{ ErrorMessage }}</span>
        </div>
        <div v-if="SuccessMessage" class="alert alert-success fade show error-message" role="alert">
            <span>{{ SuccessMessage }}</span>
        </div>
      <button class="btn btn-success" @click="sendCSV()" :disabled="runningbutton"> Send sales report and product stock as CSV to email</button>
      <h1 id="title_card" class="display-5">Products</h1>
      <div class="btn-group" role="group">
        <button :key="'all'" class="btn" :class="'all' === selectedCategory ? 'btn-success' : 'btn-secondary'" @click="changeCategory('all')">
          All
        </button>
        <button v-for="category in categories" :key="category" class="btn" :class="category === selectedCategory ? 'btn-success' : 'btn-secondary'" @click="changeCategory(category)">
          {{ category }}
        </button>
      </div>
      <p></p>
      <p></p>
      <div class="flex-row justify-content-center g-3  d-flex flex-wrap">
        <div class="c-container col-sm-12 col-md-6 col-lg-3 col-xl-3">
          <div class="card">
            <div class="front">
              <img :src=newItem.productImage class="card-img-top" alt="..." style="object-fit: cover; width: 100%; height: 50%; border-radius: 10%;">
              <div class="card-body" style=" text-align: center;">
                <h3 class="card-title">{{ newItem.productName }}</h3>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Stock:&nbsp;</span>
                  <span style="position: absolute; left:45%">{{newItem.availableStock}}{{newItem.Unit}}</span>
                </div>
                <br>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Price:&nbsp;</span>
                  <span style="position: absolute; left:45%">&#8377;{{newItem.pricePerUnit}}/{{newItem.Unit}}</span>
                </div>
              </div>
            </div>
            <div class="back">
              <br>
              <div class="card-body" style="padding-top:0; margin-top: 0;">
                <form @submit.prevent="createProduct(newItem)">
                  <div class="input-group">
                    <span for="name" class="input-group-text">Name</span>
                    <input v-model="newItem.productName" type="text" id="name" name="name" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="imageURL" class="input-group-text">Image URL</span>
                    <input v-model="newItem.productImage" type="url" id="imageURL" name="imageURL" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="quantity" class="input-group-text">Stock</span>
                    <input v-model="newItem.availableStock" type="number" id="quantity" name="quantity" min="0" max="100000" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="quantity" class="input-group-text">Expiry</span>
                    <input v-model="newItem.expiry" type="date" id="Edate" name="Edate" :min="`${new Date().toISOString().split('T')[0]}`" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="price" class="input-group-text">Price</span>
                    <input v-model="newItem.pricePerUnit" type="number" step=".01" id="price" name="price" min="0" max="1000" class="form-control">
                    <select v-model="newItem.Unit" id="unit" name="unit" class="form-select">
                      <option value="g">g</option>
                      <option value="ml">ml</option>
                      <option value="packs">packs</option>
                    </select>
                  </div>
                  <div class="input-group">
                    <span for="category" class="input-group-text">Category</span>
                    <select v-model="newItem.category" id="category" name="category" class="form-select">
                      <option v-for="category in categories" :key="category" :value=category>{{category}}</option>
                    </select>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="submit" class="btn btn-success">Create Product</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div v-for="(item, index) in filteredData" :key="item.productID" class="c-container col-sm-12 col-md-6 col-lg-3 col-xl-3" :style="{'animation-delay': index*50+'ms'}">
          <div class="card">
            <div class="front">
              <img :src=item.productImage class="card-img-top" alt="..." style="object-fit: cover; width: 100%; height: 50%; border-radius: 10%;">
              <div class="card-body" style=" text-align: center;">
                <h3 class="card-title">{{ item.productName }}</h3>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Stock:&nbsp;</span>
                  <span style="position: absolute; left:45%">{{item.availableStock+modifyQuantities[item.productID]}}{{item.Unit}}</span>
                </div>
                <br>
                <div>
                  <span style="font-weight: bold; position: absolute; right:55%">Price:&nbsp;</span>
                  <span style="position: absolute; left:45%">&#8377;{{item.pricePerUnit}}/{{item.Unit}}</span>
                </div>
              </div>
            </div>
            <div class="back">
              <br>
              <div class="card-body" style="padding-top:0; margin-top: 0;">
                <form @submit.prevent="updateProduct(item)">
                  <div class="input-group">
                    <span for="name" class="input-group-text">Name</span>
                    <input v-model="item.productName" type="text" id="name" name="name" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="imageURL" class="input-group-text">Image URL</span>
                    <input v-model="item.productImage" type="url" id="imageURL" name="imageURL" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="quantity" class="input-group-text">Restock</span>
                    <input v-model="modifyQuantities[item.productID]" type="number" id="quantity" name="quantity" :min="minQuantity(item.availableStock)" max="100000" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="quantity" class="input-group-text">Expiry</span>
                    <input v-model="modifyExpiry[item.productID]" type="date" id="Edate" name="Edate" :min="`${new Date().toISOString().split('T')[0]}`" class="form-control">
                  </div>
                  <div class="input-group">
                    <span for="price" class="input-group-text">Price</span>
                    <input v-model="item.pricePerUnit" type="number" step=".01" id="price" name="price" min="0" max="1000" class="form-control">
                    <select v-model="item.Unit" id="unit" name="unit" class="form-select">
                      <option value="g">g</option>
                      <option value="ml">ml</option>
                      <option value="packs">packs</option>
                    </select>
                  </div>
                  <div class="input-group">
                    <span for="category" class="input-group-text">Category</span>
                    <select v-model="modifyCategory[item.productID]" id="category" name="category" class="form-select">
                      <option v-for="category in categories" :key="category" :value=category>{{category}}</option>
                    </select>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-danger" @click="confirmDelete(item)">Delete</button>
                    <button type="submit" class="btn btn-success">Update</button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
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
  export default {
    name: 'itemsView',
    props: {
      search: String,
    },
    data() {
      return {
        task_ID:null,
        checkTaskInterval: null,
        categories: [],
        selectedCategory: 'all',
        apiData: [],
        dataLoading: true,
        modifyQuantities:{},
        modifyExpiry:{},
        ErrorMessage:'',
        SuccessMessage:'',
        modifyCategory:{},
        runningbutton:false,
        newItem:{
          productName:"",
          productImage:"",
          availableStock:0,
          pricePerUnit:0,
          Unit:"g",
          category:"",
          expiry:new Date().toISOString().split('T')[0]
        }
      };
    },
    mounted() {
      this.fetchItems();
    },
    computed: {
      filteredData() {
        let filtered = this.apiData
        const searchlower = this.search.toLowerCase();
        filtered = filtered.filter(item => item.productName.toLowerCase().includes(searchlower));
        if (this.selectedCategory === 'all') {
          return filtered;
        } else {
          return filtered.filter(item => item.category === this.selectedCategory);
        }
      },

    },
    beforeUnmount () {
      clearInterval(this.checkTaskInterval);
    },
    methods: {
      async sendCSV(){
        try {
          this.runningbutton=true;
          const response = await this.$axios.post(`/CSVExport`,
            {withCredentials: true});
          if (response.status === 200) {
            this.task_ID = response.data.msg;
            console.log("taskid=",this.task_ID)
            this.startCheckingTaskStatus();
          } else{
            this.runningbutton=false;
          }
        } catch (error) {
          this.runningbutton=false;
          console.error('Error:', error);
          if (error.response && error.response.data && error.response.data.msg) {
            this.ErrorMessage = error.response.data.msg;
          } else if (error.response && error.response.data && error.response.data.message) {
            this.ErrorMessage = error.response.data.msg;
          } else {
            this.ErrorMessage = 'An error occurred. Please try again later.';
          }
        }
      },
      startCheckingTaskStatus() {
        this.checkTaskInterval = setInterval(this.checkTaskStatus, 500);
      },
      async checkTaskStatus() {
        try {
          const response = await this.$axios.get(`/CSVExport/${this.task_ID}`, { withCredentials: true});
          if (response.status === 200) {
            const msg = response.data.msg;
            console.log('Task status:', response);
            if (msg === "task is still pending") {
              console.log('task is still pending'); 
            } else {
              this.runningbutton=false;
              clearInterval(this.checkTaskInterval);
              console.log('Task status:', response.data);

              const base64File1 = response.data.file1;
              const decodedFile1 = atob(base64File1);
              const blob1 = new Blob([decodedFile1]);
              const link1 = document.createElement('a');
              link1.href = URL.createObjectURL(blob1);
              link1.download = 'sales_data.csv';
              link1.click();
              alert('Sales data has been sent successfully!');
              setTimeout(function(){
              const base64File2 = response.data.file2;
              const decodedFile2 = atob(base64File2);
              const blob2 = new Blob([decodedFile2]);
              const link2 = document.createElement('a');
              link2.href = URL.createObjectURL(blob2);
              link2.download = 'stock_data.csv';
              link2.click();
              alert('Stock data has been sent successfully!');
              }, 0);
            }
          }
        } catch (error) {
          this.runningbutton=false;
          console.error('Error checking task status:', error);
        }
      },
      minQuantity(qtt) {
        return -qtt;
      },
      changeCategory(category) {
        this.selectedCategory = category;
      },
      async fetchItems() {
        try {
          const response = await this.$axios.get('/modifyProducts');
          this.apiData = response.data.msg;
          this.apiData.forEach(item => {
            this.modifyQuantities[item.productID] = 0;
            this.modifyCategory[item.productID] = item.category;
            this.modifyExpiry[item.productID] = new Date().toISOString().split('T')[0];
          });
          const resp = await this.$axios.get('/modifyCategory');
          this.categories = resp.data.msg;
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.dataLoading = false;
        }
      },
      async updateProduct(item) {
        try {
          const response = await this.$axios.patch('/modifyProducts', {
            productID: item.productID,
            productName: item.productName,
            increasedStock: this.modifyQuantities[item.productID],
            expiryDate:this.modifyExpiry[item.productID],
            productImage: item.productImage,
            category:this.modifyCategory[item.productID],
            PricePerUnit: item.PricePerUnit,
            Unit: item.Unit},
            {withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = '';
            this.SuccessMessage = response.data.msg;
            this.fetchItems();
          }
        } catch (error) {
          console.error('Error:', error);
          if (error.response && error.response.data && error.response.data.msg) {
            this.SuccessMessage = '';
            this.ErrorMessage = error.response.data.msg;
          } else {
            this.SuccessMessage = '';
            this.ErrorMessage = 'An error occurred. Please try again later.';
          }
        }
      },
      confirmDelete(item) {
        const confirmation = window.confirm(`Are you sure you want to delete ${item.productName}?`);
        if (confirmation) {
          this.deleteProduct(item);
        }
      },
      async createProduct(item){
        try {
          const response = await this.$axios.post('/modifyProducts', {
            productName:item.productName,
            productImage:item.productImage,
            availableStock:item.availableStock,
            pricePerUnit:item.pricePerUnit,
            Unit:item.Unit,
            category:item.category,
            expiryDate:item.expiry
          },{withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = '';
            this.SuccessMessage = response.data.msg;
            this.fetchItems();
            this.newItem={productName:"", productImage:"", availableStock:0, pricePerUnit:0, Unit:"g", category:"",}
          }
        } catch (error) {
          console.error('Error:', error);
          if (error.response && error.response.data && error.response.data.msg) {
            this.SuccessMessage = '';
            this.ErrorMessage = error.response.data.msg;
          } else {
            this.SuccessMessage = '';
            this.ErrorMessage = 'An error occurred. Please try again later.';
          }
        }
      },
      async deleteProduct(item) {
        try {
          const response = await this.$axios.delete(`/modifyProducts/${item.productID}`,
            {withCredentials: true});
          if (response.status === 200) {
            this.fetchItems();
          }
        } catch (error) {
          console.error('Error:', error);
          if (error.response && error.response.data && error.response.data.msg) {
            this.ErrorMessage = error.response.data.msg;
          } else if (error.response && error.response.data && error.response.data.message) {
            this.ErrorMessage = error.response.data.msg;
          } else {
            this.ErrorMessage = 'An error occurred. Please try again later.';
          }
        }
      }
    },
  };
</script>

<style scoped>
 .input-group-text{
  background-color: #42b983;
  color:white;
 }

 .input-group-text, .form-control{
  border:1px solid #999;
 }

 .input-group{
  margin:4px;
 }
</style>  