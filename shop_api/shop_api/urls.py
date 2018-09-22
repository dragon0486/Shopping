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
from django.conf.urls import url,include
from django.contrib import admin
from api.views import course,pay,weixin
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>[v1|v2]+)/', include('api.urls')),
    url(r'^test/$', course.test),

    url(r'^pay/$', pay.index),
    url(r'^pay_result/$', pay.pay_result),
    url(r'^update_order/$', pay.update_order),

    url(r'^login/$', weixin.login),
    url(r'^bind/$', weixin.bind),
    url(r'^bind_qcode/$', weixin.bind_qcode),
    url(r'^callback/$', weixin.callback),
    url(r'^sendmsg/$', weixin.sendmsg),
]
