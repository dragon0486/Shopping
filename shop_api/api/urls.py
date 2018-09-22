from django.conf.urls import url,include
from api.views import course,account,newspapers,shoppingcar,payment,alipay,order

urlpatterns = [
    # url(r'^/course/$', course.CouserView.as_view()),

    url(r'^course/$', course.CouserView.as_view({"get": "list"}), name="book_list"),
    url(r'^course/(?P<pk>\d+)/$', course.CouserView.as_view({
        'get': 'retrieve',
        # 'put': 'update',
        # 'patch': 'partial_update',
        # 'delete': 'destroy'
    }), name="book_detail"),
    url(r'^auth/$', account.AuthView.as_view()),
    url(r'^micro/$', course.MicroView.as_view()),

    url(r'^newspapers/', newspapers.NewsPapers.as_view({"get": "list"})),
    url(r'^newspapers/(?P<pk>\d+)/$', newspapers.NewsPapers.as_view({"get": "retrieve"})),

    url(r'^newspapers/(?P<pk>\d+)/agree/$', newspapers.AgreeView.as_view({'post': 'post'})),

    url(r'^shoppingcar/$', shoppingcar.ShoppingCarViewSet.as_view()),

    url(r'^payment/$', payment.PaymentViewSet.as_view()),

    url(r'^order/$', order.OrderViewSet.as_view()),
    url(r'^alipay/$', alipay.AlipayView.as_view()),
]
