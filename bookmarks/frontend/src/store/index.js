import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	alertMessage: '',
    apiUrl: 'http://127.0.0.1:8000'
  },
  mutations: {
  },
  actions: {
  },
  modules: {
  },
  getters: {
    getApiUrl: state => {
      return state.apiUrl
    }
  }
})
