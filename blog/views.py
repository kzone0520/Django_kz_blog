from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from blog.models import BlogPost
from django.urls import reverse
from blog.forms import ContentForm, CommentForm

# Create your views here.


def index(request):
    return render(request, 'blog/index.html')


def blogpost(request):
    blogs = BlogPost.objects.order_by('-date_added')
    texts = BlogPost.text
    context = {'blogs': blogs, 'texts': texts}
    return render(request, 'blog/blogpost.html', context)


def blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    text = blog.text
    comments = blog.comment_set.order_by('-date_added')
    comment_username = request.user.username
    if request.method != 'POST':
        # 如果请求不是POST则调用方法让num字段自加1
        blog.increase_num()
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # 如果是游客评论则给游客添加名字￥无名者￥
            if request.user.username:
                comment.user_name = request.user.username
            else:
                comment.user_name = '￥无名者￥'
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog:blog', args=[blog_id]))
    context = {'blog': blog, 'text': text, 'comments': comments, 'form': form,
               'comment_username': comment_username}
    return render(request, 'blog/blog.html', context)


def new_blog(request):
    # 用字符串来判断名字还是太简陋
    if request.user.username != 'kzone':
        return HttpResponse('<h1>只有管理者kzone才能添加博客~</h1>')
    if request.method != 'POST':
        form = ContentForm()
    else:
        form = ContentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:blogpost'))
    context = {'form': form}
    return render(request, 'blog/new_blog.html', context)


def edit_blog(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    blog_text = blog.text
    if request.user.username != 'kzone':
        return HttpResponse('<h1>只有管理者kzone才能修改内容~</h1>')
    if request.method != 'POST':
        form = ContentForm(instance=blog)
    else:
        form = ContentForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:blog', args=[blog.id]))
    context = {'blog': blog, 'blog_text': blog_text, 'form': form}
    return render(request, 'blog/edit_blog.html', context)


'''
这是参照书本添加条目的内容自己构想的评论页面，单独页面。
@login_required
def comment(request, blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return HttpResponseRedirect(reverse('blog:blog', args=[blog_id]))

    context = {'blog': blog, 'form': form}
    return render(request, 'blog/comment.html', context)
'''