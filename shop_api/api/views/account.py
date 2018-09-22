# -*- coding: utf-8 -*-
"""
创建时间 :
版本号 : V1
文档名 : account.py
编辑人 :
作 用 : 用户登录控制
源存储位置 : TmSccity_models\\api\\views\\user\\account.py
修改及增加功能记录 :
    修改时间 :
        1、2018/09/17:
        2、
    增加功能时间 :
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse,render
from api import models
import uuid
from utils.response import BaseResponse

class AuthView(APIView):
    # def options(self, request, *args, **kwargs):
    #     # 进行预检，返回设置响应头，才能确认浏览器下次发POST请求
    #     obj =  HttpResponse('...')
    #     obj['Access-Control-Allow-Origin'] = "*"
    #     obj['Access-Control-Allow-Headers'] = "Content-Type"
    #     return obj
    authentication_classes = []
    permission_classes = []

    def post(self,request,*args,**kwargs):
        """
            用于用户认证相关接口
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print(request.data)
        # ret = {"code":100,'data':None}
        ret = BaseResponse()
        try:
            user = request.data.get('user')
            pwd = request.data.get('pwd')
            obj = models.UserInfo.objects.filter(user=user,pwd=pwd).first()
            # obj = models.UserInfo.objects.get(user=user,pwd=pwd)
            if not user:# 简单逻辑往上放
                ret.code=400
                ret.error="错误的用户名或密码"
                return Response(ret)

            token = str(uuid.uuid4())
            models.Token.objects.update_or_create(user=obj, defaults={"token": token})  # defaults字段用于更新
            ret.token = token
        except Exception as e:
            ret.code = 1002
            ret.msg= e
        # obj = Response('...')
        # obj['Access-Control-Allow-Origin'] = "*"
        return Response(ret.dict)

    # def get(self,request,*args,**kwargs):
    #     print(request.data)
    #     return Response('...')
