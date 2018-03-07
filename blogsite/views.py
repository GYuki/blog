from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View
from django.http import HttpResponse, JsonResponse
from blogsite.models import Post, Blog, BlogSubscriber, UserPostWatched
from blogsite import forms
# Create your views here.

def get_blog_id(user_id):
    blog = Blog.objects.get(user_id=user_id)
    return blog.id

class Redirect(View):

    def get(self, request):
        if request.user.is_authenticated():
            return redirect(reverse('blogsite:feed'))
        return redirect(reverse('signupapp:login'))

class ShowBlogPosts(View):

    def get(self, request, blog_id):
        isSub = False;
        posts = Post.objects.filter(blog_id=blog_id).order_by('-created_at')
        blog = Blog.objects.filter(id=blog_id)
        if blog:
            blog_subscriber = BlogSubscriber.objects.filter(user_id=request.user.id, blog_id=blog_id)
            if blog_subscriber:
                isSub = True
            args = {'posts': posts.values(), 'blog':blog.values()[0], 'isMyPost': blog.values()[0]['user_id']==request.user.id, 'isSub': isSub}
            print ('BLOG INFO ------------------------ ', args['blog'])
            return render(request, 'blogsite/posts.html', args)
        return redirect(reverse('blogsite:feed'))


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
            return redirect(reverse('blogsite:show_post', kwargs={'post_id': post.id}))
        else:
            return HttpResponse('Not created!')

class DeletePost(View):

    def get(self, request, post_id):
        post = Post.objects.filter(id=post_id)
        if post:
            blog = Blog.objects.get(id=post.values()[0]['blog_id'])
            if request.user.id != blog.user_id:
                return redirect(reverse('blogsite:feed'))
            post.delete()
            return redirect(reverse('blogsite:posts', kwargs={'blog_id': blog.id}))
        return redirect(reverse('blogsite:feed'))

    def post(self, request):
        pass

class ShowPost(View):

    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        post.created_at = post.created_at.strftime("%d.%m.%Y %H:%M")
        blog = Blog.objects.get(id=post.blog_id)
        watch_info = UserPostWatched.objects.filter(user_id=request.user.id, post_id = post.id, seen=False)
        if watch_info:
            watch_info.update(seen=True)
        args = {'post': post, 'blog': blog, 'isMyPost': request.user.id==blog.user_id}
        return render(request, 'blogsite/post.html', args)

    def post(self, request):
        pass

class SignUnsign(View):

    def get(self, request, blog_id):
        blog_subscriber = BlogSubscriber.objects.filter(user_id=request.user.id, blog_id=blog_id)
        if blog_subscriber:
            blog_subscriber.delete()
            return redirect(reverse('blogsite:posts', kwargs={'blog_id': blog_id}))
        else:
            blog_subscriber = BlogSubscriber()
            blog_subscriber.blog_id = blog_id
            blog_subscriber.user_id = request.user.id
            blog_subscriber.save()
            return redirect(reverse('blogsite:posts', kwargs={'blog_id': blog_id}))


    def post(self, request):
        pass

class GetFreshPosts(View):

    def get(self, request):
        resp = {}
        marks = UserPostWatched.objects.filter(user_id=request.user.id, seen=False)
        if marks:
            posts_list = [x for x in marks.values()]
            resp = {'posts': posts_list, 'len': len(posts_list)}
        return JsonResponse(resp)

    def post(self, request):
        pass

class NewsFeed(View):

    def get(self, request):
        my_subcriptions = BlogSubscriber.objects.filter(user_id=request.user.id)
        blog_ids = [x['blog_id'] for x in my_subcriptions.values()]
        my_feed = Post.objects.filter(blog_id__in=blog_ids).order_by('-created_at').values()
        watch_info = UserPostWatched.objects.filter(post_id__in=[x['id'] for x in my_feed], user_id=request.user.id, seen=False).values()
        args = {'feed': my_feed, 'watches': [x['post_id'] for x in watch_info]}
        return render(request, 'blogsite/feed.html', args)

    def post(self, request):
        pass

class FreshPostsPage(View):

    def get(self, request):
        fresh_posts = UserPostWatched.objects.filter(user_id=request.user.id, seen=False)
        posts_list = Post.objects.filter(id__in=[x['post_id'] for x in fresh_posts.values()]).order_by('-created_at')
        args = {'notify': posts_list}
        return render(request, 'blogsite/notifications.html', args)

    def post(self, request):
        pass

class MarkAsWatched(View):

    def get(self, request, post_id):
        mark = UserPostWatched.objects.filter(post_id=post_id, user_id=request.user.id, seen=False)
        if mark:
            mark.update(seen=True)
        return redirect(reverse('blogsite:feed'))

    def post(self, request):
        pass

class ShowAllPosts(View):

    def get(self, request):
        post = Post.objects.all().order_by('-created_at')
        args = {'feed': post.values()}
        return render(request, 'blogsite/all_posts.html', args)

    def post(self, request):
        pass
