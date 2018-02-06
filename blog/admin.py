from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'article',)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ('title', 'desc', 'click_count',)
    list_display_links = ('title', 'desc', )
    list_editable = ('click_count',)

    fieldsets = (
        (None, {
            'fields': ('title', 'desc', 'content', 'user', 'category', 'tag', )
        }),
        ('高级设置', {
            'classes': ('collapse',),
            'fields': ('click_count', 'is_recommend',)
        }),
    )

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
