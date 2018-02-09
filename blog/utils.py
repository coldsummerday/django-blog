from django.core.cache import cache
import time
from .models import *
#利用django信号,使得model改变的时候刷新cache
from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver

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
            # 使用缓存出错，可能是没开启redis
            data = self.get_data_method(*self.args, **self.kw)
        finally:
            return data

    def set_cache(self):
        data = self.get_data_method(*self.args, **self.kw)
        cache.set(self.key, data, self.timeout)
        return data
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
    caches = {}
    caches[categoryToTagCache.key] = categoryToTagCache
    caches[categoryList.key] = categoryList

    return caches
caches = get_caches()

@receiver(pre_save,sender=Tag)
def tagUpdate(sender,**kwargs):
    global caches
    print('更新tagcache')
    caches['categoryToTagList'].set_cache()

@receiver(pre_save,sender=Category)
def categoryUpdate(sender,**kwargs):
    global caches
    print('更新catcache')
    caches['categoryToTagList'].set_cache()