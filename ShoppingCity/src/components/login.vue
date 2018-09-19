<template>
    <div>
      <h1>用户登录</h1>
      <div>
        <p><input type="text" placeholder="请输入用户名" v-model="username"/></p>
        <p><input type="text" placeholder="请输入密码" v-model="password"/></p>
        <p><input type="button" value="登录" @click="doLogin"/></p>
      </div>
    </div>
</template>

<script>
    export default {
        name: "login",
      data(){
          return{
            username:'',
            password:''
          }
      },
      methods:{
        doLogin(){
          var _this = this;
          this.$axios.request({
            url:'http://127.0.0.1:8001/api/v1/auth/',
            method:'POST',    // 不是methods
            data:{
              user:this.username,
              pwd:this.password,
            },
            headers:{
              'Content-Type':'application/json'
            }
          }).then(function (ret) {
            console.log(ret)
            if (ret.data.code == 100) {
              console.log('logining')
              // _this.$store.state.token = ret.data.token;
              // _this.$store.state.username = _this.username
              _this.$store.commit('saveToken',{token:ret.data.token,username:_this.username}) //只能传一个值
              var url = _this.$route.query.backUrl
              if(url){
                _this.$router.push({path:url})
              }else {
                _this.$router.push({path:'/index'})
              }

            } else {
              alert(ret.data.error)
            }
          }).catch(function (error) {
            console.log(error)
          })
        }
      }
    }
</script>

<style scoped>

</style>
