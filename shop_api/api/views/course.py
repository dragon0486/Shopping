from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer,BrowsableAPIRenderer
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning,BaseVersioning
from django.views import View
from .. import models
from django.shortcuts import HttpResponse
import json
from rest_framework import serializers
from rest_framework import viewsets
from api.serializers.course import *
from api.auth.auth import *
from django.contrib.contenttypes.models import ContentType

class CouserView(viewsets.ViewSetMixin,APIView):
    # renderer_classes = [JSONRenderer,]    # settings配置也可，JSONRenderer渲染器只返回json格式的数据，不渲染模板
    # versioning_class = QueryParameterVersioning # 全局配置也可，单独配置也可
    versioning_class = URLPathVersioning

    def list(self,request,*args,**kwargs):
        ret = {'code': 100, 'data': None}
        try:
            queryset = models.Course.objects.all()
            data = CourseSerializer(instance=queryset,many=True)
            ret['data'] = data.data
        except Exception as e:
            import logging
            logging.exception(e)
            ret['code']=400
        return Response(ret)

    def retrieve(self,request,*args,**kwargs):
        ret = {'code':100,'data':None}
        try:
            pk = kwargs.get('pk')
            # obj = models.Course.objects.filter(id=pk).first()
            obj = models.CourseDetail.objects.filter(course_id = pk).first()
            data = CourseDetailSerializer(instance=obj,many=False)
            ret['data'] = data.data
        except Exception as e:
            ret['code']=400
        return Response(ret)

class MicroView(APIView):
    authentication_classes = [Authentication]
    def get(self,request,*args,**kwargs):

        # token = request.query_params.get('token')
        # obj = models.Token.objects.filter(token=token).first()
        # if not obj:
        #     return Response('认证失败')
        print(request.user)
        print(request.auth)
        ret = {'code': 100, 'data': '位置为'}
        return Response(ret)

def test(request):
    # 1.在价格策略表中添加一条数据
    # models.PricePolicy.objects.create(
    #     valid_period=7,
    #     price=6.6,
    #     content_type=ContentType.objects.get(model='course'),
    #     object_id=1
    # )

    # models.PricePolicy.objects.create(
    #     valid_period=14,
    #     price=9.9,
    #     content_object=models.TopicCourse.objects.get(id=1)   # 自动找到obj对应的content_type和object_id
    # )

    # 2. 根据某个价格策略对象，找到他对应的表和数据，如：管理课程名称
    # price = models.PricePolicy.objects.get(id=2)
    # print(price.content_object.name)        # 自动帮你找到，相当于sqlalchemy的relationship

    # 3.找到某个课程关联的所有价格策略
    obj = models.TopicCourse.objects.get(id=1)
    for item in obj.policy_list.all():
        print(item.id,item.valid_period,item.price)

    return HttpResponse('...')

# class CourseViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
#     queryset = models.Course.objects.all()
#     serializer_class = CourseViewSetSerializers
