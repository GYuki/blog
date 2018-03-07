from blogsite.models import Blog

def blog_processor(request):
    blog_id = 0
    blog = Blog.objects.filter(user_id=request.user.id)
    if blog:
        blog_id = blog.values()[0]['id']
    return {'blog_ids': blog_id}
