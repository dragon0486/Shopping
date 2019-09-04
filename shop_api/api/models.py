from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.db import models
import hashlib
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(verbose_name="手机号码", max_length=15, unique=True)
    avatar = models.ImageField(upload_to='avatar', verbose_name='用户头像', null=True, blank=True,
                               help_text="头像图片的大小规格：256x256，或者对应的比例的图片")
    class Meta:
        db_table = 'luffy_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    """公共模型"""
    orders = models.IntegerField(verbose_name='显示顺序')
    is_show = models.BooleanField(verbose_name="是否上架", default=False)
    is_delete = models.BooleanField(verbose_name="逻辑删除", default=False)
    created_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, null=True, blank=True)
    updated_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, null=True, blank=True)
    class Meta:
        # 抽象模型，一般用于设置公共模型字段的，一旦设置这个相关以后，那么dajngo在数据迁移的时候就不会为这个模型单独创建一个数据表了
        abstract=True

class Banner(BaseModel):
    """轮播图"""
    # upload_to 存储子目录，真实存放地址会使用配置中的MADIE_ROOT+upload_to
    image = models.ImageField(upload_to='banner', verbose_name='轮播图', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='轮播图名称')
    note = models.CharField(max_length=150, verbose_name='备注信息')
    link = models.CharField(max_length=150, verbose_name='轮播图广告地址')
    # orders = models.IntegerField(verbose_name='显示顺序')
    # is_show=models.BooleanField(verbose_name="是否上架", default=False)
    # is_delete=models.BooleanField(verbose_name="逻辑删除", default=False)

    class Meta:
        db_table = 'luffy_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Nav(BaseModel):
    """导航"""
    NAV_POSITION = (
        (0, '顶部导航'),
        (1, '底部导航')
    )
    name = models.CharField(max_length=50, verbose_name='导航名称')
    link = models.CharField(max_length=250, verbose_name='导航地址')
    opt = models.SmallIntegerField(choices=NAV_POSITION, default=0, verbose_name='位置')

    class Meta:
        db_table = 'luffy_nav'
        verbose_name = '导航'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseCategory(BaseModel):
    """分类"""
    name = models.CharField(max_length=64, unique=True, verbose_name="分类名称")
    class Meta:
        db_table = "luffy_course_category"
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

class Course(BaseModel):
    """课程"""
    course_type = (
        (0, '付费'),
        (1, 'VIP专享'),
        (2, '学位课程')
    )
    level_choices = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    status_choices = (
        (0, '上线'),
        (1, '下线'),
        (2, '预上线'),
    )
    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="courses", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = models.TextField(max_length=2048, verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=0, verbose_name="难度等级")
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(upload_to="attachment", max_length=128, verbose_name="课件路径", blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.SET_NULL, db_constraint=False, null=True, blank=True, verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    sections = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_sections = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    class Meta:
        db_table = "luffy_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return "%s" % self.name

    @property
    def teacher_name(self):
        return self.teacher.name

    @property
    def level_name(self):
        # 难度名
        return self.get_level_display()

    @property
    def section_list(self):
        # 获取当前课程的所有章节
        coursechapter_list = self.coursechapters.filter(is_show=True, is_delete=False).order_by("chapter")
        # 通过循环当前磕碜的所有章节，来获取章节下面的所有课时
        data_list = []
        for coursechapter in coursechapter_list:
            if len(data_list) >= 4:
                break
            # 当前章节下的所有课时
            coursesection_list = coursechapter.coursesections.filter(is_show=True, is_delete=False).order_by("orders")
            # 循环每一个课时，逐个追加到data_list进行返回
            for coursesection in coursesection_list:
                if len(data_list) >= 4:
                    break
                data_list.append({
                    "id": coursesection.id,
                    "name": coursesection.name,
                    "free_trail": coursesection.free_trail,
                })

        return data_list


class Teacher(BaseModel):
    """导师"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="导师名")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="导师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="导师封面", help_text="120x120")
    brief = models.TextField(max_length=1024, verbose_name="导师描述")

    class Meta:
        db_table = "luffy_teacher"
        verbose_name = "导师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name

class CourseChapter(BaseModel):
    """章节"""
    course = models.ForeignKey("Course", related_name='coursechapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)

    class Meta:
        db_table = "luffy_course_chapter"
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)

class CourseSection(BaseModel):
    """课时"""
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='coursesections', on_delete=models.CASCADE, verbose_name="课程章节")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    orders = models.PositiveSmallIntegerField(verbose_name="课时排序")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接", help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)

    class Meta:
        db_table = "luffy_course_section"
        verbose_name = "课时"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)





