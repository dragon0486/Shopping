<template>
  <div class="note">
    <h1>微职位</h1>
    <div>{{title}}</div>
  </div>
</template>

<script>
    export default {
        name: "index",
      data(){
          return{
            title:null
          }
      },
      mounted(){
          // if(!this.$store.state.token){
          //   this.$router.push({name:'login'})
          // }
        this.initMicro()
      },
      methods:{
        initMicro(){
          var _this=this
          this.$axios.request({
            url:'http://127.0.0.1:8001/api/v1/micro/',
            method:'GET',
            params:{
              token:this.$store.state.token
            }
          }).then(function (arg) {
            if(arg.data.code===100){
              _this.title = arg.data.data
              console.log(_this.title)
            }
          })
        }
      }
    }
</script>

<style scoped>

</style>
