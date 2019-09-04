#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import random
import hashlib
from rest_framework import serializers
from rest_framework import fields
from .. import models
from django.core.cache import cache

class PasswordValidator(object):
    def __init__(self, length):
        self.length = length

    def __call__(self, value):
        if len(value) < self.length:
            message = '密码长度太短了'
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class AuthSerializer(serializers.Serializer):
    username = fields.CharField(error_messages={'required': '用户不能为空'})
    password = fields.CharField(error_messages={'required': '密码不能为空'}, validators=[PasswordValidator(3)])

class RegisterModelSerializer(serializers.ModelSerializer):
    # 只参与反序列化的插拔式字段
    sms = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.User
        fields = ('username', 'mobile', 'password', 'sms')
        extra_kwargs = {
            'sms': {
                'error_messages': {
                    'required': '验证码不能为空'
                }
            },
            'username': {
                'read_only': True
            },
            'password': {
                'write_only': True
            },
        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('手机号不合法')
        if models.User.objects.filter(mobile=value):
            raise serializers.ValidationError('账号已存在')
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('密码不合法')
        return value

    def validate(self, attrs):
        mobile = attrs.get('mobile')
        code = attrs.pop('sms')
        if int(code) != int(cache.get('sms_%s' % mobile)):
            raise serializers.ValidationError({'sms': '验证码有误'})
        attrs['username'] = mobile
        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
    
class RegisterUserNameSerializer(serializers.ModelSerializer):
    # 只参与反序列化的插拔式字段

    class Meta:
        model = models.User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {
                'write_only': True
            },
            'password': {
                'write_only': True
            },
        }

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('密码不合法')
        return value

    def validate(self, attrs):
        attrs['mobile'] = int(str(int(hashlib.md5(attrs['username'].encode()).hexdigest(),16))[:13])
        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
