"""shop_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include,re_path
from django.urls import re_path,path
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from api.views import pay,weixin,home,user,course
import xadmin
xadmin.autodiscover()
from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^api/(?P<version>[v1|v2]+)/', include('api.urls')),
    # 2019-09-03新视频添加
    url(r'^user/check_mobile/',user.CheckMobileAPIView.as_view()),
    url(r'^user/sms_code/',user.SendSMSAPIView.as_view()),
    url(r'^user/register/mobile/',user.RegisterMobileCreateAPIView.as_view()),
    url(r'^user/register/username/',user.RegisterUsernameCreateAPIView.as_view()),
    url(r'^user/register/webchat/',user.RegisterWebchatAPIView.as_view()),
    url(r'^user/login/$',user.LoginAPIView.as_view()),
    url(r'^user/login/mobile/',user.LoginMobileAPIView.as_view()),

    url(r'^home/banners', home.BannersListAPIView.as_view()),
    url(r'^home/nav/header', home.HeaderNavListAPIView.as_view()),
    url(r'^home/nav/footer', home.FooterNavListAPIView.as_view()),
    
    url(r'^course/categories/$', course.CategoryListAPIView.as_view()),
    url(r'^course/$', course.CourseListAPIView.as_view()),
    url(r'^course/(?P<pk>\d+)/$', course.CourseRetrieveAPIView.as_view()),
    url(r'^course/chapters/$', course.CourseChapterListAPIView.as_view()),

    url(r'^order/$', pay.OrderAPIView.as_view()),
    url(r'^order/aliback/', pay.AlibackAPIView.as_view()),
    #####

    url(r'^pay/$', pay.index),
    url(r'^pay_result/$', pay.pay_result),
    url(r'^update_order/$', pay.update_order),

    url(r'^login/$', weixin.login),
    url(r'^bind/$', weixin.bind),
    url(r'^bind_qcode/$', weixin.bind_qcode),
    url(r'^callback/$', weixin.callback),
    url(r'^sendmsg/$', weixin.sendmsg),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]
