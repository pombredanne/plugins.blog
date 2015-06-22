# coding: utf-8

import os

from django.core.urlresolvers import reverse
from django.db.models import QuerySet
from restify.serializers import ModelSerializer

from ..admin.forms import PostPublishForm
from ..models import Post

class PostSerializer(ModelSerializer):
    def for_list(self, post):
        return {
            'id': post.pk,
            'title': post.title,
            'created_at': post.created_at,
            'published_at': post.published_at,
            'endpoint': reverse('edit', urlconf='bangoo.plugins.blog.admin.urls', args=[post.pk], prefix='')
        }

    def get_assets(self, post):
        result = []
        assets = post.asset_set.all()
        for asset in assets:
            filename = os.path.split(asset.file.name)[-1]
            result.append(filename)
        return result

    def flatten(self, data):
        if isinstance(data, QuerySet):
            posts = []
            for post in data:
                posts.append(self.for_list(post))
            return posts
        elif isinstance(data, PostPublishForm):
            flattened = self.for_list(data.instance)
        elif hasattr(data, 'instance') and data.instance.pk:
            flattened = super(PostSerializer, self).flatten(data.instance)
            flattened['tags'] = ', '.join(_.name for _ in data.instance.tags.all())
            flattened['asset_set'] = self.get_assets(data.instance)
            flattened['url'] = reverse('api:post-api', args=[data.instance.pk])
            flattened['endpoint'] = reverse('edit', urlconf='bangoo.plugins.blog.admin.urls', args=[data.instance.pk], prefix='')
        elif isinstance(data, Post):
            flattened = super(PostSerializer, self).flatten(data)
            flattened['tags'] = ', '.join(_.name for _ in data.tags.all())
            flattened['asset_set'] = self.get_assets(data)
        else:
            flattened = super(PostSerializer, self).flatten(data)
        return flattened