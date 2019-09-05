<template>
    <div>
      <img id='avatar' :src="qcode" style="height: 100px;width: 100px;margin: 0 125px">
    </div>
</template>

<script>
    export default {
        name: "webchat_register",
      data() {
        return {
          qcode:'',
        }
      },
      created:function () {
        var _this = this;
        this.$axios.request({
            url:this.$settings.BASE_HTTP+'/user/register/webchat/',
            method:'get',    // 不是methods
          }).then(function (ret) {
            if (ret.status == 200) {
              _this.qcode = "https://login.weixin.qq.com/qrcode/"+ret.data.msg
            }
          })
      },
      mounted:function(){
        this.check_login();
      },
      methods:{
          check_login(){
            var _this = this;
        this.$axios.request({
            url:this.$settings.BASE_HTTP+'/user/register/webchat/',
            method:'POST',    // 不是methods
          }).then(function (ret) {
            console.log(ret)
            if (ret.status == 200) {
              if(ret.data.status ==408){
                _this.check_login()
              }else if (ret.data.status ==201){
                _this.qcode = ret.data.msg;
                _this.check_login()
              }else if(ret.data.status ==200){
                _this.$router.push({path:'/index'})
              }
            }
          })
          },
      }
    }
</script>

<style scoped>

</style>
