from blogsite.models import Blog, UserPostWatched

def blog_processor(request):
    blog_id = 0
    notifications = 0
    blog = Blog.objects.filter(user_id=request.user.id)
    if blog:
        blog_id = blog.values()[0]['id']
    marks = UserPostWatched.objects.filter(user_id=request.user.id, seen=False)
    if marks:
        posts_list = [x for x in marks.values()]
        notifications = len(posts_list)
    return {'blog_ids': blog_id, 'notifications_len': notifications}
