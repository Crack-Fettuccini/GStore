import { createStore } from 'vuex';
import { VuexPersistence } from 'vuex-persist';

const vuexLocal = new VuexPersistence({
  storage: window.localStorage,
});

export default createStore({
  state: {
    email: '',
    password: '',
    access_token:null,
    writtenQuantities: {}, // Add the new state for writtenQuantities
    userLevel:null,
  },
  mutations: {
    setAccessToken(state, token) {
      state.access_token = token;
    },
    setUserLevel(state, level) {
      state.userLevel = level;
    },
    updateEmail(state, newEmail) {
      state.email = newEmail;
    },
    updatePassword(state, newPassword) {
      state.password = newPassword;
    },
    updateWrittenQuantities(state, payload) {
      state.writtenQuantities = {...payload };
    },
  },
  actions: {
    resetState({ commit }) {
      commit('setAccessToken', null);
      commit('setUserLevel', null);
      commit('updateEmail', '');
      commit('updatePassword', '');
      commit('updateWrittenQuantities', {});
      localStorage.clear();
    },  },
  getters: {
      getWrittenQuantities: state => state.writtenQuantities,
  },
  plugins: [vuexLocal.plugin],

});
