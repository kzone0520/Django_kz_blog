from django import forms

from blog.models import BlogPost, Comment


class ContentForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'text']
        labels = {'title': '', 'text': ''}
        widgets = {
           'title': forms.Textarea(attrs={'cols': 40, 'rows': 1}),
           'text': forms.Textarea(attrs={'cols': 100, 'rows': 20}),
        }  #设定文本框的大小


# 这个评论框奇丑无比，可是我无能力修改了，django的文档里倒是有介绍，有兴趣的可以去看看。
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 5})}