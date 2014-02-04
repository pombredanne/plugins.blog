from django.conf.urls import patterns, url
from blog.admin import views

urlpatterns = patterns('',
    url(r'^$', views.PostList.as_view(), name='blog-admin-post-list'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_blog_post, name='blog-admin-post-edit'),
)