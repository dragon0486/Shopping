from rest_framework import serializers
from api import models
# class ArticleViewSetSerializers(serializers.ModelSerializer):
#     source = serializers.CharField(source="source.name")
#     article_type = serializers.CharField(source="get_article_type_display")
#     position = serializers.CharField(source='get_position_display')
#
#     class Meta:
#         model = models.Article
#         fields = ["title", "source", "article_type", 'head_img', 'brief', 'pub_date', 'comment_num', 'agree_num',
#                   'view_num', 'collect_num', 'position']
#
#
# class ArticleDetailViewSetSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = models.Article
#         fields = ['title', 'pub_date', 'agree_num', 'view_num', 'collect_num', 'comment_num', 'source', 'content',
#                   'head_img']