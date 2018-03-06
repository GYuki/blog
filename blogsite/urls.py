from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<blog_id>\d+)$', views.ShowBlogPosts.as_view(), name='posts'),
    url(r'^new_post/$', views.NewPost.as_view(), name='new_post'),
]
