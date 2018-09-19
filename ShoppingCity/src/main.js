// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import store from './store/store'

Vue.config.productionTip = false
//在全局变量中设置变量
Vue.prototype.$axios = axios    //this.$axios

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
//拦截器
router.beforeEach(function (to, from, next) {
  if(to.meta.requireAuth){
    // 要去的url只有登陆成功后才能访问
    if (store.state.token) {
      next()
    } else {
      next({name: 'login',query: {backUrl: to.fullPath}}) //name或者path
    }
  }else{
    next()
  }
})

