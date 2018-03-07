from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=100)

    def __str__(self):
        return self.blog_name

class Post(models.Model):
    post_header = models.CharField(max_length=100, null=False)
    post_text = models.TextField(null=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_header

class BlogSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class UserPostWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        blog = Blog.objects.create(user=kwargs['instance'], blog_name='Блог пользователя %s' %(kwargs['instance']))
        subs = BlogSubscriber.objects.create(user=kwargs['instance'], blog_id=blog.id)

def create_post(sender, **kwargs):
    if kwargs['created']:
        subs = BlogSubscriber.objects.filter(blog_id=kwargs['instance'].blog_id).values()
        sub_list = [x['user_id'] for x in subs]
        for sub in sub_list:
            mark = UserPostWatched.objects.create(user_id=sub, post_id=kwargs['instance'].id)

post_save.connect(create_profile, sender=User)
post_save.connect(create_post, sender=Post)
