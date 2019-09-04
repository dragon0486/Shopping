<template>
    <h1>支付成功，即将跳转到课程列表页面。。。</h1>
</template>

<script>
    export default {
        name: "payresult",
      mounted(){
          setTimeout(this.jumpToHome,3000)
      },
      methods:{
          jumpToHome(){
            this.$router.push({path:'/course'})
          }
      }
    }
</script>

<style scoped>

</style>
