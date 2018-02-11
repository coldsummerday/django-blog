from django.shortcuts import render,redirect
import  logging
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.conf import settings
from django.http import HttpResponse,Http404
from django.db.models import Count,Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from blog.serializers import *
# Create your views here.
from .models import *
from .forms import *
import markdown
from .utils import caches

Logger = logging.getLogger('blog.views')


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
    return (categoryList,categoryToTagList)




def page(request,article_list):
    paginator = Paginator(article_list, 5)

    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except PageNotAnInteger:
        article_list = paginator.page(1)
    except EmptyPage:
        article_list = paginator.paginator(paginator.num_pages)

    return article_list

def baseinfo():
    #除了具体的文章列表,其他 每个页面都要加载的信息
    categoryList = caches['categoryList'].get_cache()
    categoryToTagList = caches['categoryToTagList'].get_cache()
    article_list_orderby_comment = caches['article_list_orderby_comment'].get_cache()
    archive_list = caches['archive_list'].get_cache()
    try:
        article_click_queryset = Article.objects.all().order_by('click_count')[::-1][:5]
        article_click_queryset = [article for article in article_click_queryset if article.click_count!=0]
    except Exception as e:
        Logger.error(e)
    infoDir = {'categoryList':categoryList,\
                'categoryToTagList':categoryToTagList,\
                'article_list_orderby_comment':article_list_orderby_comment,\
                'archive_list':archive_list,\
                'article_click_list':article_click_queryset}
    return  infoDir
def index(request):
    #主页
    try:
        article_list = Article.objects.all()
    except Exception as e:
        Logger.error(e)

    article_list = page(request,article_list)

    return render(request,'home.html',dict({'article_list':article_list},**baseinfo()))

def search(request):
    search_text = request.GET.get('search_text')
    if not search_text:
        error_msg = "请输入关键词"
        return render(request, 'failure.html', {'reason': error_msg})
    else:
        try:
            article_list = Article.objects.filter(Q(title__icontains=search_text))
            article_list = page(request, article_list)
        except Exception as e:
            Logger.error(e)
            return render(request, 'failure.html', {'reason': e})
        return render(request, 'home.html', dict({'article_list': article_list}, **baseinfo()))



def tag_article(request,tag):
    try:
        tag_object = Tag.objects.get(name = tag)
        article_list= tag_object.article_set.all()
        article_list = page(request,article_list)
    except Tag.DoesNotExist:
        return render(request,'failure.html',{'reason':'没有找到文章'})
    except Exception as e:
        Logger.error(e)
    return render(request,'home.html',dict({'article_list':article_list},**baseinfo()))

def archive(request,year,month):
    #归档
    if month < 10:
        month = '0'+str(month)
    else:
        month = str(month)
    year = str(year)
    article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
    article_list = page(request, article_list)
    return render(request,'archive.html',dict({'article_list':article_list},**baseinfo()))


def details(request,id):
    try:
        article = Article.objects.get(pk=id)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        article.increase_click_count()
        article.content = md.convert(article.content)
        article.toc = md.toc
        categoryList, categoryToTagList = getTags()
    except Article.DoesNotExist:
        return render(request, 'failure.html', {'reason': '没有找到文章'})
    except Exception as e:
        Logger.error(e)
        return render(request, 'failure.html', {'reason': e})

    #上一页下一页信息
    try:
        if id < 2:
            before_article = None
        else:
            before_article = Article.objects.get(pk=id-1)

        next_article = Article.objects.get(pk = id + 1)
    except Article.DoesNotExist:
        next_article = None
    neighbor = articleNeighbor(before_article,next_article)


    #获取文章评论信息 ,该部分已经用restapi加ajax重写
    '''
    comments = Comment.objects.filter(article=article).order_by('id')
    #获取评论的父子关系
    comment_list = []
    comment_tree = {}
    for comment in comments:
        if comment.pid == None:
            comment_tree[comment] = {}
        else:
            find_parent_comment(comment_tree,comment)
    '''


    return render(request,'details.html',{'article':article,\
                                          'categoryList':categoryList,\
                                         'categoryToTagList':categoryToTagList,\
                                          'neighbor':neighbor,\
                                          })

def post_comment(request):
    try:
        comment_form = commentForms(request.POST)
        if comment_form.is_valid():
            pid = int(comment_form.cleaned_data["pid"])

            # 获取表单信息
            if pid == 0:
                comment = Comment.objects.create(username=comment_form.cleaned_data["username"],
                                             email=comment_form.cleaned_data["email"],
                                             content=comment_form.cleaned_data["comment"],
                                             article_id=comment_form.cleaned_data["article_id"],
                                             )
            else:
                parentComment = Comment.objects.get(pk=pid)
                article_id = comment_form.cleaned_data["article_id"]
                print(pid,parentComment.article_id,article_id)
                if str(parentComment.article_id) == str(article_id):
                    comment = Comment.objects.create(username=comment_form.cleaned_data["username"],
                                                 email=comment_form.cleaned_data["email"],
                                                 content=comment_form.cleaned_data["comment"],
                                                 article_id=comment_form.cleaned_data["article_id"],
                                                 pid = parentComment
                                                 )
                else:
                    return render(request, 'failure.html', {'reason': "文章与评论不符"})
            comment.save()
        else:
            return render(request, 'failure.html', {'reason': comment_form.errors})
    except Exception as e:
        Logger.error(e)
    return render(request, 'success.html', {'reason':"操作成功"})


def get_postComment(request,article_id,pid):
    return render(request,'postcomment.html',locals())

def find_parent_comment(commentTree,commentObj):
    for p,v in commentTree.items():
        if p.id == commentObj.pid.id:
            commentTree[p][commentObj]={}
        else:
            find_parent_comment(commentTree[p],commentObj)


class articleNeighbor(object):
    def __init__(self,before_article,next_article):
        self.before = before_article
        self.next = next_article

def pageNumberToList(list,pageNumber):
    if pageNumber ==None:
        pageNumber = 0
    else:
        pageNumber = int(pageNumber)
    eachNumber = settings.EACH_PAGE
    list_length = len(list)
    #返回不正常的分页的flag
    errorFlag = False
    if (pageNumber+1) * eachNumber >= list_length:
        end = list_length
        nextPage = False
    else:
        end = (pageNumber+1) * eachNumber
        nextPage = True
    if pageNumber * eachNumber > list_length:

        errorFlag = True
        return (errorFlag,list,False,nextPage)
    else:
        start = pageNumber * eachNumber
    beforePage = True if start>0 else False
    return (errorFlag,list[start:end],beforePage,nextPage)



##rest api
#装饰器表示允许的方法
@api_view(['GET'])
def article_index_list(request):
    if request.method == "GET":
        tagname = request.GET.get('tag')
        archiveInfo = request.GET.get('archive')
        pagenumber = request.GET.get('page',0)
        urlinfo = request.get_full_path()
        #测试get中假如有tag属性
        if tagname:
            try:
                tag_object = Tag.objects.get(name=tagname)
                article_list = tag_object.article_set.all()
                error,article_list,beforePage,nextPage =  pageNumberToList(article_list,pagenumber)
                if error:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            except (Article.DoesNotExist,Tag.DoesNotExist):
                return Response(status.HTTP_404_NOT_FOUND)
            serializer = ArticleSerializer(article_list,many=True)

            return Response({'urlinfo':urlinfo,'next':nextPage,'before':beforePage,'data':serializer.data})
        if archiveInfo and (not tagname):
            try:
                article_list = Article.objects.filter(date_publish__icontains=archiveInfo)
            except Article.DoesNotExist as e:
                Logger.log(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            error,article_list,beforePage,nextPage = pageNumberToList(article_list,pagenumber)
            serializer = ArticleSerializer(article_list,many=True)
            return Response({'urlinfo':urlinfo,'next':nextPage,'before':beforePage,'data':serializer.data})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentListApi(APIView):

    def get(self,requset,formart=None):
        if requset.GET.get('articleid'):
            articleid = requset.GET.get('articleid')
            try:
                article = Article.objects.get(pk=articleid)
                comments = Comment.objects.filter(article=article).order_by('id')
            except (Article.DoesNotExist,Comment.DoesNotExist):
                return Response("articleid error", status=status.HTTP_400_BAD_REQUEST)
            serializer = CommentSerializer(comments,many=True)
            return Response(serializer.data)
        else:
            return Response("params error", status=status.HTTP_400_BAD_REQUEST)






