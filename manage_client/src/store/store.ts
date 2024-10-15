import { createStore } from 'vuex';

const store = createStore({
  state: {
    userRole: null,
    token: null,
  },
  mutations: {
    setUserRole(state, role) {
      state.userRole = role;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  getters: {
    getToken(state) {
      return state.token; 
    },
    getUserRole(state) {
      return state.userRole; 
    },
  },
});

export default store;