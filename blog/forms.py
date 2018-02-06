from django import forms
from django.conf import settings



class commentForms(forms.Form):
    username = forms.CharField(widget=forms.TextInput(),\
                               max_length=50,error_messages={"required":"username 不能为空"})
    email = forms.EmailField(widget=forms.TextInput(), \
                             max_length=50, error_messages={"required": "email不能为空", })
    comment = forms.CharField(widget=forms.Textarea(),\
                              error_messages={"required": "评论不能为空", })
    article_id = forms.CharField(widget=forms.HiddenInput())

    pid = forms.IntegerField(widget=forms.HiddenInput())
