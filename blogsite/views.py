from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from blogsite.models import Post, Blog
from blogsite import forms
# Create your views here.

class ShowBlogPosts(View):

    def get(self, request, blog_id):
        posts = Post.objects.filter(blog_id=blog_id)
        args = {'posts': posts.values()}
        return render(request, 'blogsite/posts.html', args)

    def post(self, request):
        pass

class NewPost(View):

    def get(self, request):
        form = forms.NewPostForm()
        args = {'form': form}
        return render(request, 'blogsite/new_post.html', args)


    def get_blog_id(self, user_id):
        blog = Blog.objects.get(user_id=user_id)
        return blog.id

    def post(self, request):
        form = forms.NewPostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.post_header = form['post_header'].value()
            post.post_text = form['post_text'].value()
            post.blog_id = self.get_blog_id(request.user.id)
            post.save()
            return HttpResponse('Created')
        else:
            return HttpResponse('Not created!')

class DeletePost(View):

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id)
        if post:
            post.delete()
            return HttpResponse('Deleted')
        return HttpResponse('Not deleted')

    def post(self, request):
        pass
