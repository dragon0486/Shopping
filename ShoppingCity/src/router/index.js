import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import course from '@/components/course'
import micro from '@/components/micro'
import news from '@/components/news'
import detail from '@/components/detail'
import login from '@/components/login'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/index',
      name: 'index',
      component:Index
    },
    {
      path: '/course',
      name: 'course',
      component:course
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component:detail
    },
    {
      path: '/micro',
      name: 'micro',
      component:micro,
      meta:{
        requireAuth:true
      }
    },
    {
      path: '/news',
      name: 'news',
      component:news
    },
    {
      path: '/login',
      name: 'login',
      component:login
    },
  ],
  mode:'history'
})
