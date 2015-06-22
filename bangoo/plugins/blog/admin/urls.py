# coding: utf-8

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
   url('^$', view=views.index),
   url('posts/(?P<id>new|\d+)/$', view=views.post, name='edit')
)
