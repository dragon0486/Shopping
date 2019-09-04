<template>
    <div>
      <p><input type="text" @blur="checkMobile" placeholder="手机号码" v-model="mobile"/></p>
      <input v-model="password" type="password" placeholder="用户密码" class="user">
      <div class="sms">
          <input v-model="sms" type="text" placeholder="输入验证码" class="user">
          <span class="sms_btn" @click="send_sms">{{sms_interval_tips}}</span>
      </div>
      <button class="register_btn" @click="registerMobile">注册</button>
    </div>

</template>

<script>
    export default {
        name: "phone_register",
      data() {
        return {
          password:'',
          sms_interval_tips: "获取验证码",
          is_send: false,  // 是否在60s内发送了短信
          sms: "",
          mobile: "",
        }
      },
      methods:{
        checkMobile() {

                if (this.mobile.length < 1) {
                    return false;
                }

                // 手机号码格式是否正确
                if (!/^1[3-9]\d{9}$/.test(this.mobile)) {
                    this.$message({
                        message: "对不起！手机号码格式有误！"
                    });
                    return false;
                }

                // 验证手机号码是否已经注册了
                // this.$axios.get(this.$settings.Host+"/users/mobile/"+this.mobile+"/");
                this.$axios({
                    url: this.$settings.BASE_HTTP + '/user/check_mobile/',
                    method: 'get',
                    params: {
                        mobile: this.mobile
                    }
                }).then(response => {
                    let data = response.data;
                    window.console.log(data);
                    if (data.status != 0) {
                        this.$message({
                            message: "对不起！手机号码已经被注册！"
                        });
                        return false;
                    } else {
                        this.$message({
                            message: "该手机号码可以注册！"
                        });
                    }
                }).catch(error => {
                    let data = error.response.data;
                    this.$message({
                        message: data.message
                    })
                })

            },
        send_sms() {
                // 发送短信
                if (!/^1[3-9]\d{9}$/.test(this.mobile)) {
                    this.$message({
                        message: "对不起！手机号码格式有误！"
                    });

                    return false;
                }

                // 判断是否在60s内发送过短信
                if (this.is_send) {
                    this.$message({
                        message: "对不起,不能频繁发送短信验证！"
                    });

                    return false;
                }

                // 请求发送短信
                this.$axios({
                    url: this.$settings.BASE_HTTP + '/user/sms_code/',
                    method: 'get',
                    params: {
                        mobile: this.mobile
                    }
                }).then(response => {
                    this.$message({
                        message: response.data.msg,
                    });
                    // 修改短信的发送状态
                    this.is_send = true;

                    // 设置间隔时间60s
                    let sms_interval_time = 60;
                    // 设置短信发送间隔倒计时,.60s后把is_send改成false
                    let timer = setInterval(() => {
                        if (sms_interval_time <= 1) {
                            clearInterval(timer);
                            this.sms_interval_tips = "获取验证码";
                            this.is_send = false; // 重新回复点击发送功能的条件
                        } else {
                            sms_interval_time -= 1;
                            this.sms_interval_tips = `${sms_interval_time}秒后再次获取`;
                        }
                    }, 1000);

                }).catch(error => {
                    this.$message({
                        message: error.response.data.result,
                    })
                });

            },
        registerMobile() {
                // 注册信息提交
                if (!/^1[3-9]\d{9}$/.test(this.mobile)) {
                    this.$message({
                        message: "对不起！手机号码格式有误！"
                    });

                    return false;
                }

                if (this.sms.length < 1) {
                    this.$message({
                        message: "短信验证码不能为空！"
                    });

                    return false;
                }

                if (this.password.length < 6 || this.password.length > 16) {
                    this.$message({
                        message: "对不起，密码长度必须在6-16个字符之间！"
                    });

                    return false;
                }

                this.$axios({
                    url: this.$settings.BASE_HTTP + '/user/register/mobile/',
                    method: 'post',
                    data: {
                        mobile: this.mobile,
                        password: this.password,
                        sms: this.sms
                    }
                }).then(response => {
                    let _this = this;
                    if (response.data.status === 0){
                      _this.$message({
                        message: "注册成功！",
                        onClose() {
                            // 保存登录状态
                            // sessionStorage.user_name = response.data.user.username;
                            // sessionStorage.user_mobile = response.data.user.mobile;
                          // _this.$store.commit('saveToken',{token:_this.sms,username:_this.mobile})
                            // 跳转到用户中心
                            _this.$router.push({path:'/login'})
                        }
                    });
                    }else {  // 后台http状态码为2xx
                        // 前台逐一处理错误信息
                        window.console.log(response)
                        // this.$message({
                        //     message: response
                        // })
                    }
                }).catch(error => {
                    this.$message({
                        message: error.response.data.result
                    });
                })

            }
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
