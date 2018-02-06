from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from blog.views import *
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('archive/<int:year>/<int:month>', archive,name ='blog_archive'),
    path('', index,name='blog_home'),
    path('tags/<str:tag>',tag_article,name = 'blog_tag'),
    path('articles/<int:id>',details,name = 'blog_detail'),
    path('articles/postcommentpage/<int:article_id>/<int:pid>',get_postComment,name = 'blog_post_comment'),
    path('comment/post/',post_comment,name = "blog_post_commentform"),
    url(r'^search/$', search, name='blog_search'),
    path('articleapi/',article_index_list,name = 'blog_article_api'),
    path('articles/comment-api',CommentListApi.as_view(),name='blog_commentapi'),
]

