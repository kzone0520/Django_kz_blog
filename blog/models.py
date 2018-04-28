from django.db import models

# Create your models here.


class BlogPost(models.Model):
    title = models.TextField(max_length=200)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 博文阅读数字段
    num = models.PositiveIntegerField(default=0)

    def __str__(self):
        # 这里是为了在首页上显示出博客内容的一部分而不是全部
        if len(self.text) < 110:
            return self.text
        else:
            return self.text[:110] + '...'

    # 定义方法让阅读数自增1，然后调用save保存（参数代表只更新num字段）
    def increase_num(self):
        self.num += 1
        self.save(update_fields=['num'])


'''
原本是想照着《python编程从入门到实践》里19.1.2那样用添加新条目的方法来做添加新评论，
后来看到廖雪峰网站实战里的评论是做在每个博文页面里的，就参照那个来做了，所以这个Comment模型
将在views.blog里被引用
'''
class Comment(models.Model):
    blog = models.ForeignKey('BlogPost', on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 创建个字段用来存储评论者的名字
    user_name = models.TextField()

    def __str__(self):
        return self.text




