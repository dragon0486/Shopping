import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import course from '@/components/course'
import micro from '@/components/micro'
import news from '@/components/news'
import detail from '@/components/detail'
import payresult from '@/components/payresult'
import login from '@/components/login'
import signup from '@/components/signup'
import username_register from '@/components/username_register'
import phone_register from '@/components/phone_register'
import webchat_register from '@/components/webchat_register'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/index',
      name: 'index',
      component:Index,
      alias:'/'
    },
    {
      path: '/course',
      name: 'course',
      component:course
    },
    {
      path: '/course/detail/:course_id',
      name: 'detail',
      component:detail
    },
    {
      path: '/payresult',
      name: 'payresult',
      component:payresult
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
        {
      path: '/signup',
      name: 'signup',
      component:signup,
      children:[
        {path:'username',component:username_register},
        {path:'phone',component:phone_register},
        {path:'webchat',component:webchat_register},
      ]
    },
  ],
})
