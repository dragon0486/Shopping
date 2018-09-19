<template>
  <div class="note">
    <h1>课程详细</h1>
    <div>
      <p>{{detailMsg.course}}</p>
      <p>{{detailMsg.title}}</p>
      <p>{{detailMsg.slogon}}</p>
      <p>{{detailMsg.why}}</p>
      <p>{{detailMsg.img}}</p>
      <div>
        <ul v-for="row in detailMsg.chapter">
          <li>{{row.id}}-{{row.title}}</li>
        </ul>
      </div>
        <div>
          <h3>推荐课程</h3>
        <ul v-for="row in detailMsg.recommands">
          <li><router-link :to="{name:'detail',params:{id:row.id}}"> {{row.id}}-{{row.title}}</router-link></li>
          <li @click="changeDetail(row.id)">{{row.title}}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
      name: "index",
      data(){
        return{
          detailMsg:{}
        }
       },
      mounted(){    //如果是同一个组件内切换不同课程信息，不会触发
        var id = this.$route.params.id
        this.initDetail(id)
        console.log(this.$route,this.$router)
      },
      methods: {
        initDetail(id) {
          //axios/jquery
          var _this = this;
          this.$axios.request({
            url: 'http://127.0.0.1:8001/api/v1/course/' + id + '/',// 问题2：url后的/记得对应
            method: 'GET',
          }).then(function (data) {
            //ajax请求发送成功后获取的响应内容
            //data.data = ajax接收的data
            if (data.data.code == 100) {
              console.log(data)
              _this.detailMsg = data.data.data
            } else {
              alert('error')
            }
          }).catch(function (ret) {
            //异常自动执行400 500
          })
        },
        changeDetail(id){
          this.initDetail(id)   //主动更新内容，但url不变
          this.$router.push({name:'detail',params:{id:id}})  // 更新url，与router-link的标签功能一样
        }
      }
    }
</script>

<style scoped>

</style>
