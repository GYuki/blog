from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from blogsite.models import Post, Blog, BlogSubscriber, UserPostWatched
from blogsite import forms
# Create your views here.

def get_blog_id(user_id):
    blog = Blog.objects.get(user_id=user_id)
    return blog.id

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


    def post(self, request):
        form = forms.NewPostForm(request.POST)
        if form.is_valid():
            post = Post()
            post.post_header = form['post_header'].value()
            post.post_text = form['post_text'].value()
            post.blog_id = get_blog_id(request.user.id)
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

class ShowPost(View):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.created_at = post.created_at.strftime("%d.%m.%Y %H:%M")
        blog = Blog.objects.get(id=get_blog_id(request.user.id))
        args = {'post': post, 'blog': blog}
        return render(request, 'blogsite/post.html', args)

    def post(self, request):
        pass

class SignUnsign(View):

    def get(self, request, blog_id):
        blog_subscriber = BlogSubscriber.objects.filter(user_id=request.user.id, blog_id=blog_id)
        if blog_subscriber:
            blog_subscriber.delete()
            return HttpResponse('Unsigned')
        else:
            blog_subscriber = BlogSubscriber()
            blog_subscriber.blog_id = blog_id
            blog_subscriber.user_id = request.user.id
            blog_subscriber.save()
            return HttpResponse('Signed')

    def post(self, request):
        pass

class MarkAsRead(View):

    def get(self, request, post_id):
        mark, created = UserPostWatched.objects.get_or_create(
            user_id = request.user.id,
            post_id = post_id
        )
        if created:
            return HttpResponse('Marked')
        else:
            return HttpResponse('Already marked')

    def post(self, request):
        pass

class NewsFeed(View):

    def get(self, request):
        print (request.user.is_authenticated())
        my_subcriptions = BlogSubscriber.objects.filter(user_id=request.user.id)
        blog_ids = [x['blog_id'] for x in my_subcriptions.values()]
        my_feed = Post.objects.filter(blog_id__in=blog_ids).values()
        args = {'feed': my_feed}
        return render(request, 'blogsite/feed.html', args)

    def post(self, request):
        pass
