# coding: utf-8

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url('^$', view=views.index, name='blog-index'),
    url('^(?P<post_id>\d+)/(?P<slug>\w+)', view=views.full_post, name='blog-full-post'),
    url('^tag/(?P<tag>\w+)/', view=views.index, name='blog-tagged-posts')
)