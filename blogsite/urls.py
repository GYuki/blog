from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<blog_id>\d+)$', views.ShowBlogPosts.as_view(), name='posts'),
    url(r'^new_post/$', views.NewPost.as_view(), name='new_post'),
    url(r'^delete_post/(?P<post_id>\d+)$', views.DeletePost.as_view(), name='delete_post'),
]
