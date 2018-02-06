# -*- coding: utf-8 -*-
from django import template
import re
register = template.Library()

# 定义一个将日期中的月份转换为大写的过滤器，如8转换为八
@register.filter(name = 'month_to_upper')
def month_to_upper(key):
    return ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'][key.month-1]

# 注册过滤器
#register.filter('month_to_upper', month_to_upper)

indent_base = 30




##递归建立评论树,,,,其实应该在把字典传过去然后前端用js去解析的
##有已用ajax 获取comment 然后js 去更新,此tag无效
def recursive_build_tree(html_ele,tree,indent):
    for k,v in tree.items():
        row = '''<li class="item clearfix" style="margin-left: %spx;">
        <div class="comment-main">
         <header class="comment-header">
          <div class="comment-meta">
           <a class="comment-author" href="mailto:%s">%s</a> 评论于
           <time >%s</time>
          </div>
         </header>
         <div class="comment-body">
          <p><a href="mailto:%s">@%s</a> %s
          <button type="button" class="btn btn-info"
           style="float: right;" onclick=" opencomment('%s')">回复他/她</button></p>
         </div>
        </div> </li>
        ''' % (indent, k.email, k.username, \
               k.date_publish.strftime('%Y-%m-%d'), \
               k.pid.email, k.pid.username, k.content,k.id)

        html_ele += row
        if v:
            html_ele =  recursive_build_tree(html_ele,tree[k],indent+indent_base)

    return html_ele

@register.simple_tag
def build_comment_tree(comment_tree):
    html_ele = "";
    for k,v in comment_tree.items():
        row = '''<li class="item clearfix" style="margin-left: 5px;"> 
   <div class="comment-main"> 
    <header class="comment-header"> 
     <div class="comment-meta"> 
      <a class="comment-author" href="mailto:%s">%s</a> 评论于 
      <time >%s</time> 
     </div> 
    </header> 
    <div class="comment-body"> 
     <p> %s<button type="button" class="btn btn-info" style="float: right;" onclick=" opencomment('%s')">回复他/她</button></p> 
    </div> 
   </div> </li>
            ''' %(k.email,k.username,k.date_publish.strftime('%Y-%m-%d'),k.content,k.id)
        html_ele += row
        if len(v.items())>1:
            html_ele = recursive_build_tree(html_ele,v,indent_base)
    return html_ele +''




