from django.shortcuts import render
from django.views import View
from blogsite.models import Post, Blog
# Create your views here.

class ShowBlogPosts(View):

    def get(self, request, blog_id):
        print (blog_id)
        posts = Post.objects.filter(blog_id=blog_id)
        args = {'posts': posts.values()}
        return render(request, 'blogsite/posts.html', args)

    def post(self, request):
        pass
