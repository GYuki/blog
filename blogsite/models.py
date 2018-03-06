from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=100)

class Post(models.Model):
    post_header = models.CharField(max_length=100, null=False)
    post_text = models.TextField(null=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BlogSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

class UserPostWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

def create_profile(sender, **kwargs):
    print (kwargs['instance'])
    if kwargs['created']:
        blog = Blog.objects.create(user=kwargs['instance'], blog_name='Блог пользователя %s' %(kwargs['instance']))

post_save.connect(create_profile, sender=User)
