from rest_framework import serializers
from .. import models
class BannersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ('image', 'link')

class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nav
        fields = ('name', 'link')


