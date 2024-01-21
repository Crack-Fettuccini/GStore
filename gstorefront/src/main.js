import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import store from './store'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

const axiosInstance = axios.create({
    withCredentials: true,
    baseURL: 'https://127.0.0.1:8100',
    timeout: 5000,
});
axiosInstance.interceptors.request.use(
  (config) => {
    const accessToken = store.state.access_token;
    if (accessToken) {
      config.headers['Authorization'] = 'Bearer ' + accessToken;
    }
    return config;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      store.dispatch('resetState');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      // Handle 401 error globally
      store.dispatch('resetState');
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  if (requiresAuth) {
    try {
      let response = await axiosInstance.get('/refreshJWTToken');
      if (response.status === 200) {
          store.commit('setAccessToken', response.data.accessToken);
          store.commit('setUserLevel', response.data.userLevel);
        }
    } catch (error) {
        console.error('Error:', error);
        if (error.response && error.response.data) {
          console.log(error.response.data);
        } else {
          console.log('An error occurred. Please try again later.');
        }
      }

    const userLevel = store.state.userLevel;
    const accessToken = store.state.access_token;

    if (!accessToken || !userLevel) {
      next({ path: '/login' });
    } else {
      const allowedLevels = {
        'user': ['U'],
        'manager': ['M'],
        'admin': ['A']
      };

      const routeLevel = to.meta.level;
      
      if (allowedLevels[routeLevel]){
        if (allowedLevels[routeLevel].includes(userLevel)) {
          next();
        } else if (userLevel==='U'){
          next({ path: '/user/dashboard' });
        } else if (userLevel==='M'){
          next({ path: '/manager/dashboard' });
        } else if (userLevel==='A'){
          next({ path: '/admin/dashboard' });
        } else{
          next({ path: '/login' });
        }
      } else {
        next({ path: '/login' });
      }
    }
  } else {
    next();
  }
});

const app = createApp(App);
app.config.globalProperties.$axios = axiosInstance;
app.use(router);
app.use(store);
app.mount('#app');
