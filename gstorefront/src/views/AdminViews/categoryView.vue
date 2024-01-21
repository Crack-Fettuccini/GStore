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
      <h1 id="title_card" class="display-5">Update Categories</h1>
      <table class="table table-striped">
        <tr v-for="category in categories" :key="category" >
          <th scope="col">
            <form @submit.prevent="updateCategory(category, renamedCategories[category])" style="background-color:transparent;">
              <div class="input-group" style="border-radius:6px !important; background-color: white;">
                <span class="input-group-text" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);">Rename </span>
                <span class="input-group-text" style="background-color: #42b983;  border-color: #42b983; color:white;">{{ category }}</span>
                <span class="input-group-text" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);"> as </span>
                <input type="text" ref="renamecat" class="form-control" v-model="renamedCategories[category]" placeholder="Category Name" aria-describedby="button-addon2">
                <button class="btn btn-outline-success" type="submit" id="update">Update Category</button>
              </div>
            </form>
          </th>
          <th scope="col">
            <form @submit.prevent="deleteCategory(category, movedCategories[category])" style="background-color:transparent;">
              <div class="input-group">
                <span class="input-group-text" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);"> Move </span>
                <span class="input-group-text" style="background-color: #42b983; border-color: #42b983; color:white;">{{ category }}</span>
                <span class="input-group-text" style="color:white; background-color: rgb(255,100,60); border-color: rgb(255,110,85);"> to </span>
                <select ref="changecat" id="category" name="category" v-model="movedCategories[category]" class="form-select">
                  <option v-for="cat in filteredCategories(category)" :key="cat" :value=cat>{{cat}}</option>
                </select>
                <button class="btn btn-danger" type="submit" id="delete">Delete Category</button>
              </div>
            </form>
          </th>
        </tr>
        <tr>
          <th scope="col">
            <form @submit.prevent="createCategory(newcategory)" style="background-color:transparent;">
              <div class="input-group" >
                <input type="text" class="form-control" placeholder="Category Name" v-model="newcategory" aria-label="Recipient's username" aria-describedby="button-addon2">
                <button class="btn btn-success" type="submit" id="create">Create New Category</button>
              </div>
            </form>
          </th>
        </tr>
      </table>
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
        newcategory:'',
        dataLoading: true,
        categories:[],
        renamedCategories: {},
        movedCategories: {},
        SuccessMessage:"",
        ErrorMessage:"",
      };
    },
    mounted() {
      this.fetchCategories();
    },
    methods: {
      async fetchCategories() {
        try {
          const resp = await this.$axios.get('/modifyCategory');
          this.categories = resp.data.msg;
          this.categories.forEach((category) => {
            this.renamedCategories[category]='';
            this.movedCategories[category]=this.filteredCategories(category)[0];
          });
        } catch (error) {
          console.error('Error fetching data:', error);
        } finally {
          this.dataLoading = false;
        }
      },
      filteredCategories(currentCategory) {
        return this.categories.filter((cat) => cat !== currentCategory);
      },
      async updateCategory(category, renamedValue) {
        try {
          const response = await this.$axios.patch('/modifyCategory',
          {categoryOld:category,
            categoryNew:renamedValue},
          {withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = null;
            this.SuccessMessage = response.data.msg;
            this.fetchCategories();
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
      deleteCategory(category, moveto) {
        const confirmation = window.confirm(`Are you sure you want to move items in ${category} to ${moveto}?`);
        if (confirmation) {
          this.moveCategory(category, moveto);
        }
      },
      async moveCategory(category, moveto) {
        try {
          const response = await this.$axios.delete(`/modifyCategory/${category}/${moveto}`, {withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = null;
            this.SuccessMessage = response.data.msg;
            this.fetchCategories();
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
      async createCategory(category){
        try {
          const response = await this.$axios.post('/modifyCategory',
          {newCategory:category},
          {withCredentials: true});
          if (response.status === 200) {
            this.ErrorMessage = null;
            this.SuccessMessage = response.data.msg;
            this.fetchCategories();
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
      }
    },
  };
</script>
  