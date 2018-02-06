from django.db import models
from  django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='photo/%Y/%m',default='photo/default.png',\
                               max_length=200,blank=True, null=True, verbose_name='用户头像')
    qq = models.CharField(max_length=20,blank=True,null=True,verbose_name="QQ号码")
    mobile = models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name="手机号码")
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name="个人网页地址")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username
    def __unicode__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=30,verbose_name="分类名称")
    index = models.IntegerField(default=999,verbose_name="分类的排序")

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name="标签名称")
    category = models.ManyToManyField(Category,verbose_name="分类")

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name



#自定义数据管理器
#1. 新加一个数据处理方法
class ArticleManager(models.Manager):

    def objects(self):
        return super(ArticleManager, self).objects()
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y年%m月文章归档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=50,verbose_name='文章描述')
    content = models.TextField(verbose_name="文章内容")
    click_count = models.IntegerField(default=0,verbose_name='浏览量')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name="发布时间")

    user = models.ForeignKey(User,verbose_name="用户",on_delete=models.CASCADE)
    category = models.ForeignKey(Category,blank=True,null=True,verbose_name="分类",on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag,verbose_name="标签")

    objects = ArticleManager()

    class Meta:
        verbose_name='文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def increase_click_count(self):
        self.click_count += 1
        self.save(update_fields=['click_count'])

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='用户名')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱地址')
    #url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    #user = models.ForeignKey(User, blank=True, null=True, verbose_name='用户',on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, verbose_name='文章',on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, verbose_name='父级评论',on_delete=models.CASCADE)
    #记录子评论列表

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


