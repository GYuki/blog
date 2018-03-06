from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=100)

class Post(models.Model):
    post_header = models.CharField(max_length=100, null=False)
    post_text = models.TextField(null=False)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class BlogSubscriber(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE)

class UserPostWatched(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
