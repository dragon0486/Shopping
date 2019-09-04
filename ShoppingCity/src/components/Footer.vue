<template>
    <div class="footer">
        <ul>
            <!--<li>关于我们</li>-->
            <!--<li>联系我们</li>-->
            <!--<li>商务合作</li>-->
            <!--<li>帮助中心</li>-->
            <!--<li>意见反馈</li>-->
            <!--<li>新手指南</li>-->
            <li v-for="nav in nav_list">
                <!--<router-link :to="nav.link">-->
                  {{ nav.name }}
                <!--</router-link>-->
            </li>
        </ul>
        <p>Copyright © luffycity.com版权所有 | 京ICP备17072161号-1</p>
    </div>
</template>

<script>
    export default {
        name: "Footer",
        data() {
            return {
                nav_list: []
            }
        },
      created() {
            this.$axios({
                url: this.$settings.BASE_HTTP + '/home/nav/footer'
            }).then(response => {
                this.nav_list = response.data.results
            })
        },
    }
</script>

<style scoped>
    .footer {
        width: 100%;
        height: 128px;
        background: #25292e;
        color: #fff;
    }

    .footer ul {
        margin: 0 auto 16px;
        padding-top: 38px;
        width: 810px;
    }

    .footer ul li {
        float: left;
        width: 112px;
        margin: 0 10px;
        text-align: center;
        font-size: 14px;
    }

    .footer ul::after {
        content: "";
        display: block;
        clear: both;
    }

    .footer p {
        text-align: center;
        font-size: 12px;
    }
</style>
