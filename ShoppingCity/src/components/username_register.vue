<template>
    <div>
      <p><input type="text" placeholder="请输入用户名" v-model="username"/></p>
      <p><input type="password" placeholder="请输入密码"  v-model="password"/></p>
      <p><input type="password" placeholder="请再次输入密码" @blur="checkPassword" v-model="password2"/></p>
      <button class="register_btn" @click="registerUserName">注册</button>
    </div>

</template>

<script>
    export default {
        name: "username_register",
      data() {
        return {
          username:'',
          password:'',
          password2:'',
          pwd_confirm:false
        }
      },
      methods:{
        registerUserName(method){

          if(!this.pwd_confirm){
            this.$message({
                    message: "两次输入密码不一致"
                });
                return false;
          }

          var _this = this;
          this.$axios.request({
            url:this.$settings.BASE_HTTP+'/user/register/username/',
            method:'POST',    // 不是methods
            data:{
              username:this.username,
              password:this.password,
            },
          }).then(function (response) {
            if (response.data.status === 0) {
                _this.$message({
                    message: "注册成功！",
                    onClose() {
                        // 保存登录状态
                        // sessionStorage.user_name = response.data.user.username;
                        // sessionStorage.user_mobile = response.data.user.mobile;
                        // _this.$store.state.token = ret.data.token;
                        // _this.$store.state.username = _this.username
                      // _this.$store.commit('saveToken',{token:_this.password,username:_this.username})
                        // 跳转到用户中心
                        _this.$router.push({path:'/login'})
                    }
                });
            } else {
              alert(response.data.msg)
            }
          }).catch(function (error) {
            console.log(error)
          })
        },
        checkPassword() {

            // 手机号码格式是否正确
            if (this.password!=this.password2) {
                this.$message({
                    message: "两次输入密码不一致"
                });
                return false;
            }else{
              this.pwd_confirm=true
            }
        },
      }
    }
</script>

<style scoped>
.box {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .box img {
        width: 100%;
        min-height: 100%;
    }

    .box .register {
        position: absolute;
        width: 500px;
        height: 400px;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
        top: -238px;
    }

    .register .register-title {
        width: 100%;
        font-size: 24px;
        text-align: center;
        padding-top: 30px;
        padding-bottom: 30px;
        color: #4a4a4a;
        letter-spacing: .39px;
    }

    .register-title img {
        width: 190px;
        height: auto;
    }

    .register-title p {
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .register_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .register_box .title {
        font-size: 20px;
        color: #9b9b9b;
        letter-spacing: .32px;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        justify-content: space-around;
        padding: 50px 60px 0 60px;
        margin-bottom: 20px;
        cursor: pointer;
    }

    .register_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .inp {
        width: 350px;
        margin: 0 auto;
    }

    .inp input {
        outline: 0;
        width: 100%;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp input.user {
        margin-bottom: 16px;
    }

    .inp .rember {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-top: 10px;
    }

    .inp .rember p:first-of-type {
        font-size: 12px;
        color: #4a4a4a;
        letter-spacing: .19px;
        margin-left: 22px;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        /*position: relative;*/
    }

    .inp .rember p:nth-of-type(2) {
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .19px;
        cursor: pointer;
    }

    .inp .rember input {
        outline: 0;
        width: 30px;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp .rember p span {
        display: inline-block;
        font-size: 12px;
        width: 100px;
        /*position: absolute;*/
        /*left: 20px;*/

    }

    #geetest {
        margin-top: 20px;
    }

    .register_btn {
        width: 100%;
        height: 45px;
        background: #84cc39;
        border-radius: 5px;
        font-size: 16px;
        color: #fff;
        letter-spacing: .26px;
        margin-top: 30px;
    }

    .inp .go_login {
        text-align: center;
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .26px;
        padding-top: 20px;
    }

    .inp .go_login a {
        color: #84cc39;
        cursor: pointer;
    }

    .sms {
        position: relative;
    }

    .sms .sms_btn {
        position: absolute;
        top: -12px;
        right: 0;
        bottom: 0;
        margin: auto;
        width: 130px;
        text-align: center;
        height: 24px;
        color: #ff7000;
        cursor: pointer;
        border-left: 1px solid #999;
    }
</style>
