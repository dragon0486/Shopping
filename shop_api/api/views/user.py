import re
import random
import json
import requests
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from .. import models, serializers, throttles
from api.serializers import auth
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework_jwt.serializers import jwt_encode_handler
from utils.APIResponse import APIResponse

client = AcsClient('LTAIW2njpzYPpEZV', 'xUwDppwYAqFw2JMJ0ALolm9JYJKrN8', 'cn-hangzhou')
qcode = None
tip = 1
ctime=None
ticket_dict = {}
USER_INIT_DICT = {}
ALL_COOKIE_DICT = {}
        
# 校验手机号基类
class CheckMobileBaseAPIView(APIView):
    def check_mobile(self, request):
        request_data = request.query_params
        mobile = request_data.get('mobile')
        if not mobile:
            return APIResponse(1, '手机号不能为空'), None
        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1, '手机号有误'), None
        return None, mobile
    
# 发送验证码
class SendSMSAPIView(CheckMobileBaseAPIView):
    throttle_classes = [throttles.SMSRateThrottle]
    def get(self, request, *args, **kwargs):
        error_response, mobile = self.check_mobile(request)
        if error_response:
            return error_response

        # 验证码
        code = int("".join([str(random.randint(0,9)) for _ in range(6)]))
        # 发送验证码
        result = sms_code_send(mobile, code)
        # 发送验证码结果判定
        if not result:
            return APIResponse(1, '验证码发送失败')
        # 存储到redis
        cache.set('sms_%s' % mobile, code, 60*60*24)
        # 成功结果
        return APIResponse(0, '验证码发送成功')

# 手机号校验
class CheckMobileAPIView(CheckMobileBaseAPIView):
    def get(self, request, *args, **kwargs):
        error_response, mobile = self.check_mobile(request)
        if error_response:
            return error_response

        user_obj = models.User.objects.filter(mobile=mobile)
        if user_obj:
            return APIResponse(1, '手机号已存在')
        return APIResponse(0, 'ok')

# 手机号注册
# 自动：序列化，在serializer里面写好验证方法
class RegisterMobileCreateAPIView(CreateAPIView):
    queryset = models.User.objects
    serializer_class = auth.RegisterModelSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse(0, 'ok', user=response.data)

class RegisterUsernameCreateAPIView(CreateAPIView):
    queryset = models.User.objects
    serializer_class = auth.RegisterUserNameSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return APIResponse(0, 'ok', user=response.data)

class RegisterWebchatAPIView(APIView):
    def get(self, request, *args, **kwargs):
        global ctime
        ctime = time.time()  # 时间窗，用于生成请求url
        response = requests.get(
            url='https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&fun=new&lang=zh_CN&_=%s' % ctime
            # r后面一般是时间窗，redirect_url=xxx完成操作后跳转url，可以删除
        )
        code = re.findall('uuid = "(.*)";', response.text)
        global qcode
        qcode = code[0]
        return APIResponse(1000, qcode)

    def post(self, request, *args, **kwargs):
        global qcode
        global tip
        global ctime
        data = {"msg": "success", "code": 408}
        r1 = requests.get(
            url='https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=%s&tip=%s&sr=-1767722401&_=%s' % (
                qcode, tip, ctime,)  # 传请求二维码的参数
        )
        # 这时向微信请求，pending多久看微信什么时候返回
        if 'window.code=408' in r1.text:
            print('无人扫码')
            data["msg"] = "waiting"
        elif 'window.code=201' in r1.text:  # 已扫码，返回头像url给前端，再继续监听同一个url看是否确认
            data['code'] = 201
            avatar = re.findall("window.userAvatar = '(.*)';", r1.text)[0]
            data['msg'] = avatar
            tip = 0  # 修改一下请求url的参数
        elif 'window.code=200' in r1.text:  # 已确认
            ALL_COOKIE_DICT.update(r1.cookies.get_dict())  # 更新第一次确认的cookie，可能有用
            redirect_url = re.findall('window.redirect_uri="(.*)";', r1.text)[0]  # 不同设备重定向url可能不一样
            redirect_url = redirect_url + "&fun=new&version=v2&lang=zh_CN"  # 新的重定向url添加后缀去请求用户数据
            r2 = requests.get(url=redirect_url)
            # 获取凭证
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r2.text, 'html.parser')
            for tag in soup.find('error').children:  # 找到所有的登陆凭证
                ticket_dict[tag.name] = tag.get_text()  # 字典类型，引用类型，修改值不用global
            ALL_COOKIE_DICT.update(r2.cookies.get_dict())  # 更新重定向的cookie，可能有用
            data['code'] = 200
            user_info_url = "https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1780597526&lang=zh_CN&pass_ticket=" + \
                            ticket_dict['pass_ticket']
            user_info_data = {
                'BaseRequest': {
                    'DeviceID': "e459555225169136",  # 这个随便写，没获取过
                    'Sid': ticket_dict['wxsid'],
                    'Skey': ticket_dict['skey'],  # 全部在用户凭证里
                    'Uin': ticket_dict['wxuin'],
                }
            }
            r3 = requests.post(
                url=user_info_url,
                json=user_info_data,  # 不能data，否则只能拿到key，value传不了
            )
            r3.encoding = 'utf-8'  # 编码
            user_init_dict = json.loads(r3.text)  # loads将text字符串类型转为字典类型
            ALL_COOKIE_DICT.update(r3.cookies.get_dict())  # 再次保存cookie，这样就包含了以上所有流程的cookie
            # USER_INIT_DICT 已声明为空字典，内存地址已有，添加值不修改地址，但赋值会改变地址，比如=123，之前要声明global即可。
            # USER_INIT_DICT['123']=123,    USER_INIT_DICT.update(user_init_dict)两种做法都没改变地址
            USER_INIT_DICT.update(user_init_dict)
        return APIResponse(data['code'], data['msg'])

# 手动
class RegisterMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        mobile = request_data.get('mobile')
        password = request_data.get('password')
        code = request_data.get('sms')

        if not (mobile and password and code):
            return APIResponse(1, '注册信息有误')

        # 校验验证码
        if code != cache.get('sms_%s' % mobile):
            return APIResponse(1, '验证码有误')

        # 校验账号
        if models.User.objects.filter(mobile=mobile):
            return APIResponse(1, '用户已存在')

        # 校验        密码
        if len(password) < 6:
            return APIResponse(1, '密码不合法')

        try:
            user_obj = models.User.objects.create_user(username=mobile, mobile=mobile, password=password)
            return APIResponse(0, '注册成功')
        except:
            return APIResponse(1, '注册失败')

def sms_code_send(phone_number,sms_code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', str(phone_number))
    request.add_query_param('SignName', "路飞vue")
    request.add_query_param('TemplateCode', "SMS_173251941")
    request.add_query_param('TemplateParam', json.dumps({"code":sms_code}))

    response = client.do_action(request)
    return json.loads(str(response, encoding='utf-8'))

# 多方式登录
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not (username and password):
            return APIResponse(1, '用户名密码有误')
        # 多方式登录
        if re.match(r'^1[3-9][0-9]{9}$', username):
            user_obj = models.User.objects.filter(mobile=username, is_active=True).first()
            if not user_obj.check_password(password):
                user_obj = None
        else:
            from django.contrib import auth
            user_obj = auth.authenticate(username=username, password=password)
            if not (user_obj and user_obj.is_active):
                return APIResponse(1, '用户未激活')
        if user_obj:
            payload = jwt_payload_handler(user_obj)
            token = jwt_encode_handler(payload)
            return APIResponse(0, 'ok', results={
                'username': user_obj.username,
                'mobile': user_obj.mobile,
                'token': token
            })
        else:
            return APIResponse(1, '用户名密码有误')
        
# 手机号登陆
class LoginMobileAPIView(APIView):
    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        code = request.data.get('sms')
        if not (mobile and code):
            return APIResponse(1, '信息有误')

        user_obj = models.User.objects.filter(mobile=mobile).first()
        if not user_obj:
            return APIResponse(1, '手机号未注册')

        if int(code) != int(cache.get('sms_%s' % mobile)):
            return APIResponse(1, '验证码有误')

        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        return APIResponse(0, 'ok', token=token, user={
            'username': user_obj.username,
            'mobile': user_obj.mobile,
        })