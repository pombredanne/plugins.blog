# coding: utf-8

from bangoo.admin.api import api

from .api.resources import PostResource

FRONTEND_URLCONF = 'bangoo.plugins.blog.urls'
BACKEND_URLCONF = 'bangoo.plugins.blog.admin.urls'

api.register(regex='blog/(?P<post_id>(\d+|publish|list|new))/$', resource=PostResource)
