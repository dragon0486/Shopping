from django.shortcuts import render,redirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from utils.pay import AliPay
import time
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.APIResponse import APIResponse
from rest_framework.response import Response
from django.core.cache import cache

def aliPay():
    # 沙箱测试地址：https://openhome.alipay.com/platform/appDaily.htm?tab=info
    # 支付相关配置
    APPID = "2016092200570009"
    # APPID = "2016092200570009" # 线上的应用需要支付宝审核通过后appid才生效
    NOTIFY_URL = "http://127.0.0.1:8000/order/aliback/"   # 需公网IP
    RETURN_URL = "http://127.0.0.1:8000/order/aliback/"
    PRI_KEY_PATH = "api/keys/app_private_2048.txt"
    PUB_KEY_PATH = "api/keys/alipay_public_2048.txt"

    obj = AliPay(
        appid=APPID,
        app_notify_url=NOTIFY_URL,  # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成）
        return_url=RETURN_URL,  # 如果支付成功，重定向回到你的网站的地址。
        alipay_public_key_path=settings.PUB_KEY_PATH,  # 支付宝公钥
        app_private_key_path=settings.PRI_KEY_PATH,  # 应用私钥
        debug=True,  # 默认False,
    )
    return obj

class OrderAPIView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        alipay = aliPay()
        trade_no = str(time.time()).replace('.', '1')
        # 考虑信息安全性，订单最终的金额一定是前后台双方校验决定
        subject = request.data.get('subject')
        money = request.data.get('money')

        # 对信息要进行校验
        if not (subject and money):
            return APIResponse(1, '订单信息有误！')

        query_params = alipay.direct_pay(
            subject=subject,
            out_trade_no=trade_no,
            total_amount=money,
        )
        trade_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

        # 服务器存储订单信息：订单状态 False - 未支付 - mysql中也需要存储 order id no status user_id
        cache.set(trade_no, False)

        return APIResponse(0, 'ok', {
            'trade_no': trade_no,
            'trade_url': trade_url
        })

class AlibackAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 初始化alipay
        alipay = aliPay()
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]
        logging.warning("^_^: %s" % post_dict)

        sign = post_dict.pop('sign', None)
        # 通过调用alipay的verify方法去二次认证
        status = alipay.verify(post_dict, sign)
        if status:  # 订单状态在此修改
            logging.warning("^_^: %s" % post_dict)
            pass
        return Response('验证成功')

    def get(self, request, *args, **kwargs):
        # 初始化alipay
        alipay = aliPay()

        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        if status:
            # 获取订单状态，显示给用户
            return Response('支付成功')

def index(request):
    if request.method == 'GET':
        return render(request,'index.html')

    alipay = aliPay()
    # 对购买的数据进行加密
    money = float(request.POST.get('price'))        # 拿到浮点型小数
    out_trade_no = "x2" + str(time.time())          # 随机生成的订单号
    # 1. 在数据库创建一条数据：状态（待支付）
    # 2. 创建加密的数据，然后放到url发送给支付宝
    query_params = alipay.direct_pay(
        subject="python之路",  # 商品简单描述
        out_trade_no= out_trade_no,  # 商户订单号，支付完成后支付宝会返回订单号
        total_amount=money,  # 交易金额(单位: 元 保留俩位小数)
    )
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    return redirect(pay_url)

def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None) # 获取sign对应的签名，通过verify函数检验
    alipay = aliPay()
    status = alipay.verify(params, sign)    # true or false

    if status:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')

@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        from urllib.parse import parse_qs

        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]         # 解析字典

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 这一步去数据库修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print(out_trade_no)
            # 2. 根据订单号将数据库中的数据进行更新
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    return HttpResponse('')