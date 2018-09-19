from .. import models
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['title','course_img','level','id']
    level = serializers.CharField(source='get_level_display')

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseDetail
        fields = ['slogon','why','course','recommands','title','img','level','level_name','chapter']

    title = serializers.CharField(source='course.title')    # title不一定非得model字段，配置source即可
    img = serializers.CharField(source='course.course_img')
    level = serializers.CharField(source='course.level')    # 显示中文obj.get_level_display()
    level_name = serializers.CharField(source='course.get_level_display')   # 默认会判断加括号
    recommands = serializers.SerializerMethodField()
    chapter = serializers.SerializerMethodField()
    def get_recommands(self,obj):
        # 获取推荐的所有课程
        queryset = obj.recommend_courses.all()
        return [{'id':row.id,'title':row.title} for row in queryset]
    def get_chapter(self,obj):
        queryset = obj.course.chapter_set.all()     # 外键反向查找
        return [{'id': row.num, 'title': row.name} for row in queryset]