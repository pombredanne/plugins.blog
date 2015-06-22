# coding: utf-8

from django.shortcuts import render, get_object_or_404
from taggit.models import Tag

from .models import Post


def index(request, **kwargs):
    if request.user.is_superuser:
        qs = Post.objects.all()
    else:
        qs = Post.objects.filter(published_at__isnull=False).all()

    if 'tag' in kwargs:
        qs = qs.filter(tags__name=kwargs['tag'])

    tags = Tag.objects.all()

    args = {
        'posts': qs,
        'tags': tags
    }

    return render(request, 'blog/index.html', args)


def full_post(request, post_id, **kwargs):
    if request.user.is_superuser:
        post = get_object_or_404(Post, pk=post_id)
    else:
        post = get_object_or_404(Post, pk=post_id, published_at__isnull=False)

    tags = Tag.objects.all()

    args = {
        'post': post,
        'tags': tags
    }

    return render(request, 'blog/post.html', args)
