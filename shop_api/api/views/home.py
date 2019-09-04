from rest_framework.generics import ListAPIView
from .. import models
from api.serializers import home
class BannersListAPIView(ListAPIView):
    queryset = models.Banner.objects.filter(is_show=True, is_delete=False)
    serializer_class = home.BannersModelSerializer

class HeaderNavListAPIView(ListAPIView):
    queryset = models.Nav.objects.filter(is_show=True, is_delete=False, opt=0).order_by('orders')
    serializer_class = home.NavModelSerializer

class FooterNavListAPIView(ListAPIView):
    queryset = models.Nav.objects.filter(is_show=True, is_delete=False, opt=1).order_by('orders')
    serializer_class = home.NavModelSerializer
