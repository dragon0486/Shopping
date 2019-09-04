<template>
  <div>
    <Banner></Banner>
  </div>
</template>

<script>
  import Banner from "@/components/Banner"
  export default {
    name: "Index",
    components:{
      Banner
    },
    data() {
      return {
        msg: '首页'
      }
    }
  }
</script>

<style scoped>

</style>
