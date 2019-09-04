<template>
    <el-carousel height="520px" :interval="3000" arrow="always">
        <!--<el-carousel-item>-->
            <!--<img src="../assets/img/banner1.png" alt="">-->
        <!--</el-carousel-item>-->
        <!--<el-carousel-item>-->
            <!--<img src="../assets/img/banner2.png" alt="">-->
        <!--</el-carousel-item>-->
        <!--<el-carousel-item>-->
            <!--<img src="../assets/img/banner3.png" alt="">-->
        <!--</el-carousel-item>-->
      <el-carousel-item v-for="banner in banner_list" :key="banner.link">
            <a :href="banner.link">
                <img :src="banner.image" alt="">
            </a>
            <!--<router-link :to="banner.link">-->
                <!--<img :src="banner.image" alt="">-->
            <!--</router-link>-->
        </el-carousel-item>
    </el-carousel>
</template>
<!---->
<script>
    export default {
        name: "Banner",
        data() {
            return {
                banner_list: []
            }
        },
        created () {
          this.$axios({
                url: this.$settings.BASE_HTTP +'/home/banners',
                method: 'get',
            }).then(response => {
                // window.console.log(response.data);
                let data = response.data.results;
                this.banner_list = data;
            })
        },
    }
</script>

<style scoped>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 18px;
        opacity: 0.75;
        line-height: 300px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }
    img {
        text-align: center;
        height: 520px;
    }
</style>
