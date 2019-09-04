import Vue from 'vue'
import Vuex from 'vuex'
import Cookie from 'vue-cookies'

Vue.use(Vuex)

export default new Vuex.Store({
  // 组件中通过 this.$store.state.username 调用
  state: {
    username:Cookie.get('username'),
    token:Cookie.get('token'),
    mobile:Cookie.get('mobile'),
    apiList:{
      course: 'http://127.0.0.1:8000/api/v1/course/',
      courseDetail: 'http://127.0.0.1:8000/api/v1/course/',
      auth: 'http://127.0.0.1:8000/api/v1/auth/',
      micro: 'http://127.0.0.1:8000/api/v1/micro/'
    }
  },
  mutations: {
    // 组件中通过 this.$store.commit(saveToken,参数)  调用
    saveToken: function (state, userToken) {
      state.username = userToken.username;
      state.token = userToken.token;
      state.mobile = userToken.mobile;
      Cookie.set("username", userToken.username, "20min")
      Cookie.set("token", userToken.token, "20min")
      Cookie.set("mobile", userToken.mobile, "20min")

    },
    clearToken: function (state) {
      state.username = null
      state.token = null
      state.mobile = null
      Cookie.remove('username')
      Cookie.remove('token')
      Cookie.remove('mobile')

    }
  }
})
