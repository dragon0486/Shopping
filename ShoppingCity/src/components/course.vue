<template>
  <div>
    <h1>{{msg}}</h1>
    <!--<ul v-for="item in courseList">-->
      <!--<li ></li>-->
    <!--</ul>-->
    <div v-for="item in courseList">
      <div style="width: 350px;float:left;">
        <img :src="item.course_img"/>
        <router-link :to="{name:'detail',params:{id:item.id}}">{{item.title}}</router-link>
        <p>{{item.level}}</p>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
      name: "index",    // 问题1：起名不能带.
      data(){
        return{
          msg:"课程列表",
          courseList:[

          ]
        }
      },
      mounted(){
        this.initCourse()
      },
      methods:{
        initCourse(){
          //axios/jquery
          var _this = this;
          this.$axios.request({
            url:'http://127.0.0.1:8001/api/v1/course/',// 问题2：url后的/记得对应
            method:'GET',
          }).then(function (data) {
            //ajax请求发送成功后获取的响应内容
            //data.data = ajax接收的data
            if(data.data.code == 100){
              _this.courseList = data.data.data
            }else{
              alert('error')
            }
          }).catch(function (ret) {
            //异常自动执行400 500
          })
        }
      }
    }
</script>

<style scoped>

</style>
