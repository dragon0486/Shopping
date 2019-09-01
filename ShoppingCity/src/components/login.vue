<template>
    <div>
      <h1>用户登录</h1>
      <div>
        <p><input type="text" placeholder="请输入用户名" v-model="username"/></p>
        <p><input type="text" placeholder="请输入密码" v-model="password"/></p>
        <p><input type="button" value="登录" @click="doLogin"/></p>
      </div>

      <h1>微信登录</h1>
      <div>
        <p>扫码</p>
        <img id='avatar' :src="qcode" style="height: 100px;width: 100px">
      </div>

      <h1>手机登录</h1>
      <div>
        <p><input type="text" placeholder="手机号" v-model="phone"/></p>
        <p><input type="text" placeholder="验证码" v-model="code"/><input type="button" value="获取验证码" @click="getSmsCode"/></p>
        <p><input type="button" value="登录" @click="doLogin('phone number')"/></p>
      </div>
    </div>
</template>

<script>
    export default {
        name: "login",
      data(){
          return{
            username:'',
            password:'',
            qcode:""
          }
      },
      created:function () {
        var _this = this;
        this.$axios.request({
            url:'http://127.0.0.1:8000/user/login',
            method:'POST',    // 不是methods
            data:{
              login_method:'webchat'
            },
            headers:{
              'Content-Type':'application/json'
            }
          }).then(function (ret) {
            console.log("logging")
            if (ret.status == 200) {
              _this.qcode = "https://login.weixin.qq.com/qrcode/"+ret.data.data.msg
            }
          })
      },
      mounted:function(){
          console.log("checking ")
        this.check_login();
      },
      methods:{
          check_login(){
            console.log("checking ")
            var _this = this;
        this.$axios.request({
            url:'http://127.0.0.1:8000/user/login',
            method:'POST',    // 不是methods
            data:{
              login_method:'webchat_check'
            },
            headers:{
              'Content-Type':'application/json'
            }
          }).then(function (ret) {
            console.log(ret)
            if (ret.status == 200) {
              if(ret.data.data.code ==408){
                _this.check_login()
              }else if (ret.data.data.code ==201){
                _this.qcode = ret.data.data.msg;
                _this.check_login()
              }else if(ret.data.data.code ==200){
                _this.$router.push({path:'/index'})
              }
            }
          })
          },
        doLogin(method){
          var _this = this;
          this.$axios.request({
            url:'http://127.0.0.1:8000/user/login',
            method:'POST',    // 不是methods
            data:{
              user:this.username,
              pwd:this.password,
              phone:this.phone,
              code:this.code,
              login_method:method
            },
            headers:{
              'Content-Type':'application/json'
            }
          }).then(function (ret) {
            console.log(ret)
            if (ret.status == 200) {
              console.log('logining')
              // _this.$store.state.token = ret.data.token;
              // _this.$store.state.username = _this.username
              _this.$store.commit('saveToken',{token:_this.code,username:_this.phone}) //只能传一个值
              var url = _this.$route.query.backUrl
              if(url){
                _this.$router.push({path:url})
              }else {
                _this.$router.push({path:'/index'})
              }

            } else {
              alert(ret.data.data.msg)
            }
          }).catch(function (error) {
            console.log(error)
          })
        },
        getSmsCode(){
          var _this = this;
          this.$axios.request({
            url:'http://127.0.0.1:8000/user/login',
            method:'POST',    // 不是methods
            data:{
              phone_number:this.phone,
              login_method:"phone verify"
            },
            headers:{
              'Content-Type':'application/json'
            }
          }).then(function (ret) {
            console.log(ret)
            if (ret.status == 200) {
              console.log('got code is',ret.data.data.msg)
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
