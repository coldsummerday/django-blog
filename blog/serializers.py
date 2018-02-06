from rest_framework import serializers
from blog.models import Article,Comment

##该类提供Model类到json序列化与反序列化的方法,方便rest api调用


class ArticleSerializer(serializers.ModelSerializer):
    date_publish_str = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ('id','title','desc','click_count','date_publish_str','comment_count')

    def get_comment_count(self,obj):
        return len(obj.comment_set.all())

    def get_date_publish_str(self,obj):
        return obj.date_publish.strftime('%Y-%m-%d')



class CommentSerializer(serializers.ModelSerializer):
    date_publish_str = serializers.SerializerMethodField()
    pid_email = serializers.SerializerMethodField()
    pid_username = serializers.SerializerMethodField()
    pid_id = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id','email','username','date_publish_str','pid_email','pid_username','content','pid_id')

    def get_date_publish_str(self,comentObj):
        return  comentObj.date_publish.strftime('%Y-%m-%d')

    def get_pid_id(self,commentObj):
        if commentObj.pid == None:
            return
        else:
            return commentObj.pid.id

    def get_pid_email(self,commentObj):
        if commentObj.pid==None:
            return
        else:
            return commentObj.pid.email
    def get_pid_username(self,commentObj):
        if commentObj.pid == None:
            return
        else:
            return commentObj.pid.username





