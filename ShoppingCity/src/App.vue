<template>
  <div id="app">
      <div class="header">
            <div class="header-slogan">老男孩IT教育集团 | 帮助有志向的年轻人通过努力学习获得体面的工作和生活！</div>
            <div class="header-nav">
                <h1 class="header-logo"></h1>
                <ul class="header-menu">
                    <li v-for="nav in nav_list" :key="nav.link">
                        <span @click="togglePage(nav.link)" :class="page==nav.link?'this':''"><router-link :to="nav.link">{{ nav.name }}</router-link></span>
                    </li>
                    <!--<li :class="{active: page == 'index'}" @click="togglePage('index')"><router-link to="/index">首页</router-link></li>-->
                    <!--<li :class="{active: page == 'course'}" @click="togglePage('course')"><router-link to="/course">课程</router-link></li>-->
                    <!--<li :class="{active: page == 'micro'}" @click="togglePage('micro')"><router-link to="/micro">微职位</router-link></li>-->
                    <!--<li :class="{active: page == 'news'}" @click="togglePage('news')"><router-link to="/news">深科技</router-link></li>-->
                </ul>
                <div class="header-owner">
                    <div class="shop-cart full-left">
                        <img src="./assets/img/cart.svg" alt="">
                        <span><router-link to="/cart">购物车</router-link></span>
                    </div>
                    <div v-if="this.$store.state.token||session.token">
                        <a>{{this.$store.state.username||session.user_name}}</a>
                        <a @click="doLogout">注销</a>
                    </div>
                    <div v-else>
                        <router-link to="/login">登录</router-link>&nbsp;|&nbsp;
                        <router-link to="/signup/phone">注册</router-link>
                    </div>
                </div>
            </div>
        </div>
    <div class="body">
      <router-view/>
    </div>
    <!--<div class="footer"></div>-->
    <Footer></Footer>
  </div>
</template>

<script>
  import Footer from "@/components/Footer"
export default {
  name: 'App',
      data(){
          return{
            is_logout: true,
            page: '/index',
            nav_list: [],
            session:sessionStorage
          }
      },
  components:{
    Footer
  },
  created() {
      this.page = localStorage.page;
      this.$axios({
          url: this.$settings.BASE_HTTP + '/home/nav/header'
      }).then(response => {
          this.nav_list = response.data.results
      })
  },
  methods:{
    doLogout(){
      this.$store.commit('clearToken');
      this.$router.push({path:'/login'})
    },
    togglePage(page) {
                this.page = page;
            }
  }
}
</script>

<style>
        .header {
            width: 100%;
            background-color: #ccc;
            /*position: fixed;*/
        }
        .header-slogan {
            width: 1200px;
            font: normal 14px/36px '微软雅黑';
            color: #333;
            margin: 0 auto;
        }
        .header-nav {
            width: 1200px;
            margin: 0 auto;
            /*background-color: orange;*/
        }
        .header-nav:after {
            content: "";
            display: block;
            clear: both;
        }
        .header-logo, .header-menu {
            float: left;
        }
        .header-owner {
            float: right;
        }
        .header-logo {
            width: 118px;
            height: 36px;
            background: url("../static/header-logo.svg") no-repeat;
        }
        .header-menu {
            margin-left: 40px;
        }
        .header-menu li {
            float: left;
            margin-top: 26px;
            cursor: pointer;
            margin-right: 20px;
        }
        .header-menu li:hover {
            color: #444;
            padding-bottom: 5px;
            border-bottom: 2px solid #444;
        }
        .header-owner {
            padding-top: 26px;
        }
        .active {
            color: #444;
            padding-bottom: 5px;
            border-bottom: 2px solid #444;
        }
        .body {
            width: 1200px;
            margin: 0 auto;
        }
        ul {
            margin: 0;
            padding: 0;
            list-style: none;
        }

    /*全局*/
    /* 工具的全局样式 */
    .full-left {
        float: left !important;
    }

    .full-right {
        float: right !important;
    }
</style>
