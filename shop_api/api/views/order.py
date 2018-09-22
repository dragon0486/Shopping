import json
import time
import datetime
import random
from rest_framework.views import APIView
from rest_framework.response import Response

from django.conf import settings
from django.db import transaction
from django.db.models import F

from api.auth.auth import Authentication
from api.auth.permission import ShopPermission
from utils.response import BaseResponse
from api import models
from utils import redis_pool
from api.views.pay import aliPay

def generate_order_num():
    """
    生成订单编号, 且必须唯一
    :return:
    """
    while True:
        order_num = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(111, 999))
        if not models.Order.objects.filter(order_number=order_num).exists():
            break
    return order_num

def generate_transaction_num():
    """
    生成流水编号, 且必须唯一
    :return:
    """
    while True:
        transaction_number = time.strftime('%Y%m%d%H%M%S', time.localtime()) + str(random.randint(111, 999))
        if not models.TransactionRecord.objects.filter(transaction_number=transaction_number).exists():
            break
    return transaction_number

class OrderViewSet(APIView):
    authentication_classes = [Authentication, ]
    permission_classes = [ShopPermission, ]
    def post(self,request,*args,**kwargs):
        """
        立即支付
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        """
        1. 获取用户提交数据
                {
                    balance:1000,抵扣的贝里
                    money:900，账单金额
                }
           balance = request.data.get("balance")
           money = request.data.get("money")
           
        2. 数据验证
            - 大于等于0
            - 个人账户是否有1000贝里
            
            if user.auth.user.balance < balance:
                账户贝里余额不足
                
        优惠券ID_LIST = [1,3,4]
        总价
        实际支付
        3. 去结算中获取课程信息
            for course_dict in redis的结算中获取：
                # 获取课程ID
                # 根据course_id去数据库检查状态
                
                # 获取价格策略
                # 根据policy_id去数据库检查是否还依然存在
                
                # 获取使用优惠券ID
                # 根据优惠券ID检查优惠券是否过期
                
                # 获取原价+获取优惠券类型
                    - 立减
                        0 = 获取原价 - 优惠券金额
                        或
                        折后价格 = 获取原价 - 优惠券金额
                    - 满减：是否满足限制
                        折后价格 = 获取原价 - 优惠券金额
                    - 折扣：
                        折后价格 = 获取原价 * 80 / 100
                        
        4. 全站优惠券
            - 去数据库校验全站优惠券的合法性
            - 应用优惠券：
                - 立减
                    0 = 实际支付 - 优惠券金额
                    或
                    折后价格 =实际支付 - 优惠券金额
                - 满减：是否满足限制
                    折后价格 = 实际支付 - 优惠券金额
                - 折扣：
                    折后价格 = 实际支付 * 80 / 100
            - 实际支付
        5. 贝里抵扣
        
        6. 总金额校验
            实际支付 - 贝里 = money:900
        
        7. 为当前课程生成订单
            
                - 订单表创建一条数据 Order
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                    - 订单详细表创建一条数据 OrderDetail   EnrolledCourse
                
                - 如果有贝里支付
                    - 贝里金额扣除  Account
                    - 交易记录     TransactionRecord
                
                - 优惠券状态更新   CouponRecord
                
                注意：
                    如果支付宝支付金额0，  表示订单状态：已支付
                    如果支付宝支付金额110，表示订单状态：未支付
                        - 生成URL（含订单号）
                        - 回调函数：更新订单状态
                    
        """

        """
        redis = {
            payment_1_2:{
                course_id:2,
                'title': 'CRM客户关系管理系统实战开发-专题', 
                'img': 'CRM.jpg', 'policy_id': '4', 
                'coupon': {}, 
                'default_coupon': 0, 
                'period': 210, 'period_display': '12个月', 'price': 122.0}, 
            },
            payment_1_1:{
                course_id:1,
                'title': '爬虫开发-专题', 
                'img': '爬虫开发-专题.jpg', 
                'policy_id': '2', 
                'coupon': {
                    4: {'coupon_type': 0, 'coupon_display': '立减券', 'money_equivalent_value': 40}, 
                    6: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 60, 'minimum_consume': 100}
                }, 
                'default_coupon': 0, 
                'period': 60, 
                'period_display': '2个月', 
                'price': 599.0}
            },
            payment_global_coupon_1:{
                'coupon': {
                    2: {'coupon_type': 1, 'coupon_display': '满减券', 'money_equivalent_value': 200, 'minimum_consume': 500}
                }, 
                'default_coupon': 0
            }
        }
        """
        ret = BaseResponse()
        try:
            # 用户请求验证
            alipay = request.data.get('alipay')  # >= 0
            balance = request.data.get('balance')  # >= 0

            if balance > request.user.balance:
                ret.code = 4002
                ret.error = "账户中贝里余额不足"
                return Response(ret.dict)

            # luffy_payment_1_*
            redis_payment_key = settings.PAYMENT_KEY %(request.auth.user_id,"*",)
            # luffy_payment_coupon_1
            redis_global_coupon_key = settings.PAYMENT_COUPON_KEY %(request.auth.user_id,)

            # 1. 获取绑定课程信息
            course_list = []
            for key in redis_pool.conn.scan_iter(redis_payment_key):
                info = {}
                data = redis_pool.conn.hgetall(key)   # 所有的购买课程
                for k,v in data.items():
                    kk = k.decode('utf-8')
                    if kk == "coupon":
                        info[kk] = json.loads(v.decode('utf-8'))
                    else:
                        info[kk] = v.decode('utf-8')
                course_list.append(info)

            # 2.全站优惠券
            global_coupon_dict = {
                'coupon':json.loads(redis_pool.conn.hget(redis_global_coupon_key,'coupon').decode('utf-8')),
                'default_coupon':redis_pool.conn.hget(redis_global_coupon_key,'default_coupon').decode('utf-8')
            }

            # 当前时间
            current_date = datetime.datetime.now().date()
            current_datetime = datetime.datetime.now()

            # 原价
            total_price = 0
            # 总抵扣的钱
            discount = 0
            # 购买课程和使用的优惠券id
            buy_course_record = []
            use_coupon_record_id_list = []

            for cp in course_list:
                _policy_id = int(cp['policy_id'])
                _course_id = int(cp['course_id'])
                _coupon_record_id = int(cp['default_coupon'])

                temp = {
                    'course_id': _course_id,
                    'course_name': "course",
                    'valid_period': cp['period'],  # 有效期：30
                    'period': cp['period_display'],  # 有效期：一个月
                    'original_price': float(cp['price']),
                    'price': 0,
                }

                # 计算购买原总价
                total_price += float(cp['price'])

                # 未使用单课程优惠券
                if _coupon_record_id == 0:
                    temp['price'] = cp['price']
                    buy_course_record.append(temp)
                    continue
                print(cp['course_id'])
                # 课程是否已经下线或价格策略被修改
                policy_object = models.PricePolicy.objects.get(id=_policy_id)  # 价格策略对象
                course_object = policy_object.content_object  # 课程对象

                if course_object.id != _course_id:
                    raise Exception('课程和价格策略对应失败')
                if course_object.status != 0:
                    raise Exception('课程已下线，无法购买')

                # 选择的优惠券是否在缓存中
                if _coupon_record_id not in cp['coupon']:
                    ret.code = 1010
                    ret.error = "课程优惠券不存在"
                    return Response(ret.dict)
                choose_coupon = cp['coupon']['_coupon_record_id']
                # 根据优惠券ID检查优惠券是否过期
                coupon_obj = models.CouponRecord.objects.filter(id=_coupon_record_id).first()

                valid_begin_date = coupon_obj.coupon.valid_begin_date
                valid_end_date = coupon_obj.coupon.valid_end_date
                if valid_begin_date:
                    if current_date < valid_begin_date:
                        raise Exception('优惠券使用还未到时间')
                if valid_end_date:
                    if current_date > valid_end_date:
                        raise Exception('优惠券已过期')

                # 使用的是单课程优惠券抵扣了多少钱；使用的 个人优惠券ID
                if choose_coupon['coupon_type'] == 0:
                    # 通用优惠券
                    money = choose_coupon['money_equivalent_value']
                    discount += money
                elif choose_coupon['coupon_type'] == 1:
                    # 满减券
                    money = choose_coupon['money_equivalent_value']
                    minimum_consume = choose_coupon['minimum_consume']
                    if policy_object.price >= minimum_consume:
                        discount += money
                elif choose_coupon['coupon_type'] == 2:
                    # 打折券
                    money = policy_object.price * choose_coupon['off_percent']
                    discount += money

                temp['price'] = cp['price'] - money
                buy_course_record.append(temp)
                use_coupon_record_id_list.append(_coupon_record_id)

            _default_coupon = int(global_coupon_dict['default_coupon'])
            # 未使用全局优惠券时总价和折扣价格不需改变
            if not _default_coupon == 0:

                # 全局优惠券是否在数据库存在或者过期
                choosen_global_coupon_obj = models.CouponRecord.objects.filter(id=_default_coupon).first().coupon
                if not choosen_global_coupon_obj:
                    ret.code = 4003
                    ret.error = "全站优惠券不存在"
                    return Response(ret.dict)

                begin_date = choosen_global_coupon_obj.valid_begin_date
                end_date = choosen_global_coupon_obj.valid_end_date
                if begin_date:
                    if current_date < begin_date:
                        raise Exception('优惠券使用还未到时间')
                if end_date:
                    if current_date > end_date:
                        raise Exception('优惠券已过期')

                # 使用全局优惠券抵扣了多少钱
                if choosen_global_coupon_obj.coupon_type == 0:
                    # 通用优惠券
                    money = choosen_global_coupon_obj.money_equivalent_value
                    discount += money
                elif choosen_global_coupon_obj.coupon_type == 1:
                    # 满减券
                    money = choosen_global_coupon_obj.money_equivalent_value
                    minimum_consume = choosen_global_coupon_obj.minimum_consume
                    if (total_price - discount) >= minimum_consume:
                        discount += money
                elif choosen_global_coupon_obj.coupon_type == 2:
                    # 打折券
                    money = (total_price - discount) * choosen_global_coupon_obj.off_percent
                    discount += money

            # 贝里抵扣的钱
            if balance:
                discount += balance

            if (alipay + discount) != total_price:
                ret.code = 4001
                ret.error = "总价、优惠券抵扣、贝里抵扣和实际支付的金额不符"
                return Response(ret.dict)

            # 创建订单 + 支付宝支付
            # 创建订单详细
            # 贝里抵扣 + 贝里记录
            # 优惠券状态更新
            actual_amount = 0
            if alipay:
                payment_type = 1  # 支付宝
                actual_amount = alipay
            elif balance:
                payment_type = 3  # 贝里
            else:
                payment_type = 2  # 优惠码

            with transaction.atomic():
                order_num = generate_order_num()
                if payment_type == 1:
                    order_object = models.Order.objects.create(
                        payment_type=payment_type,
                        order_number=order_num,
                        account=request.user,
                        actual_amount=actual_amount,
                        status=1,  # 待支付
                    )
                else:
                    order_object = models.Order.objects.create(
                        payment_type=payment_type,
                        order_number=order_num,
                        account=request.user,
                        actual_amount=actual_amount,
                        status=0,  # 支付成功，优惠券和贝里已够支付
                        pay_time=current_datetime
                    )
                for item in buy_course_record:

                    detail = models.OrderDetail.objects.create(
                        order=order_object,
                        content_object=models.Course.objects.get(id=item['course_id']),
                        original_price=item['original_price'],
                        price=item['price'],
                        valid_period_display=item['period'],
                        valid_period=item['valid_period']
                    )
                models.Account.objects.filter(id=request.user.id).update(balance=F('balance') - balance)

                models.TransactionRecord.objects.create(
                    account=request.user,
                    amount=request.user.balance,
                    balance=request.user.balance - balance,
                    transaction_type=1,
                    content_object=order_object,
                    transaction_number=generate_transaction_num()
                )
                effect_row = models.CouponRecord.objects.filter(id__in=use_coupon_record_id_list).update(
                    order=order_object,
                    used_time=current_datetime)

                if effect_row != len(use_coupon_record_id_list):
                    raise Exception('优惠券使用失败')

                ret.payment_type = payment_type
                # 生成支付宝URL地址
                if payment_type == 1:
                    pay = aliPay()      # 配置好信息
                    query_params = pay.direct_pay(
                        subject="路飞学城",  # 商品简单描述
                        out_trade_no=order_num,  # 商户订单号
                        total_amount=actual_amount,  # 交易金额(单位: 元 保留俩位小数)
                    )
                    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)

                    ret.pay_url = pay_url

        except IndentationError as e:
            ret.code = 4000
            ret.msg = str(e)

        return Response(ret.dict)
