from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^posts/(?P<blog_id>\d+)$', views.ShowBlogPosts.as_view(), name='posts'),
    url(r'^all_feed/$', views.ShowAllPosts.as_view(), name='all_posts'),
    url(r'^new_post/$', views.NewPost.as_view(), name='new_post'),
    url(r'^delete_post/(?P<post_id>\d+)$', views.DeletePost.as_view(), name='delete_post'),
    url(r'^post/(?P<post_id>\d+)$', views.ShowPost.as_view(), name='show_post'),
    url(r'^sign_unsign/(?P<blog_id>\d+)$', views.SignUnsign.as_view(), name='sign_unsign'),
    url(r'^fresh_posts/$', views.GetFreshPosts.as_view(), name='fresh_posts'),
    url(r'^feed/$', views.NewsFeed.as_view(), name='feed'),
    url(r'^notify/$', views.FreshPostsPage.as_view(), name='notify'),
    url(r'^mark_watched/(?P<post_id>\d+)$', views.MarkAsWatched.as_view(), name='mark_watched'),
]
