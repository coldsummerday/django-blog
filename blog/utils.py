from django.core.cache import cache
import time
from .models import *
#利用django信号,使得model改变的时候刷新cache
from django.core.signals import request_finished
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import Count
import  logging
Logger = logging.getLogger('blog.views')
##改用redis缓存来解决分类与标签的问题

# 获取和设置缓存的类
class RedisCache():
    def __init__(self, key, timeout, get_data_method, args=None, kw=None):
        self.key = key
        self.timeout = timeout
        self.get_data_method = get_data_method
        self.args = [] if args is None else args
        self.kw = {} if kw is None else kw

    def get_cache(self):
        try:
            # 判断缓存是否存在
            if cache.has_key(self.key):
                data = cache.get(self.key)
            else:
                data = self.set_cache()
        except Exception as e:
            Logger.log(e)
            # 使用缓存出错，可能是没开启redis,重新获取所需data
            data = self.get_data_method(*self.args, **self.kw)
        finally:
            return data

    #重新从数据库中取数据
    def set_cache(self):
        data = self.get_data_method(*self.args, **self.kw)
        cache.set(self.key, data, self.timeout)
        return data

    def update_cache(self,data):
        cache.set(self.key,data,self.timeout)


class categoryToTag(object):
    def __init__(self,category,tag):
        self.category = category
        self.tag = tag
def getTags():
    try:
        tags = Tag.objects.all()
    except Exception as e:
        Logger.error(e)
    categoryList = []
    categoryToTagList = []
    for tag in tags:
        categorys = tag.category.all()
        if categorys:
            for category in categorys:
                if category.name not in categoryList:
                    categoryList.append(category.name)
                categoryToTagList.append(categoryToTag(category.name, tag.name))
    return categoryToTagList

def getArticleOrByCom():
    try:
        comment_count_queryset = Comment.objects.values('article').annotate(comment_count=Count('article'))
        article_list_orderby_comment = [{'article': Article.objects.get(pk=comment['article']), \
                                     'comment_count': comment['comment_count']} \
                                    for comment in comment_count_queryset][::-1]
        if len(article_list_orderby_comment) > 6:
            article_list_orderby_comment = article_list_orderby_comment[:5]
        return article_list_orderby_comment
    except Exception as e:
        Logger.log(e)
        return []



def getArchive():
    try:
        archive_list = Article.objects.distinct_date()
        return archive_list
    except Exception as e:
        Logger.log(e)
        return []


def getCategory():
    try:
        categorys = Category.objects.all()
        categoryList = []
        for category in categorys:
            categoryList.append(category.name)
        return categoryList
    except Exception as e:
        Logger.log(e)
    return []

def get_caches():
    categoryToTagCache = RedisCache('categoryToTagList',60*60*24,getTags)
    categoryList = RedisCache('categoryList',60*60*24,getCategory)
    article_list_orderby_comment = RedisCache('article_list_orderby_comment',60*60*24,getArticleOrByCom)
    archive_list  = RedisCache('archive_list',60*60*24,getArchive)
    caches = {}
    caches[categoryToTagCache.key] = categoryToTagCache
    caches[categoryList.key] = categoryList
    caches[article_list_orderby_comment.key] = article_list_orderby_comment
    caches[archive_list.key] = archive_list
    return caches
caches = get_caches()




@receiver([post_save,post_delete],sender=Tag)
def tagUpdate(sender,**kwargs):
    global caches
    caches['categoryToTagList'].set_cache()

@receiver([post_save,post_delete],sender=Category)
def categoryUpdate(sender,**kwargs):
    global caches
    caches['categoryToTagList'].set_cache()


@receiver([post_delete,post_save],sender = Comment)
def CommentUpdate(sender,**kwargs):
    global caches
    caches['article_list_orderby_comment'].set_cache()