from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<blog_id>\d+)$', views.ShowBlogPosts.as_view(), name='posts'),
]
