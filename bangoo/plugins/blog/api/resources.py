# coding: utf-8

import json

from django.shortcuts import get_object_or_404
from restify.http import status
from restify.http.response import ApiResponse
from restify.resource import ModelResource

from ..admin.forms import PostForm, PostPublishForm
from ..models import Post
from ..api.serializers import PostSerializer

class PostResource(ModelResource):
    class Meta:
        resource_name = 'post-api'
        serializer = PostSerializer

    def get(self, request, post_id):
        if post_id == 'list':
            posts = Post.objects.filter(author=request.user).all()
            return ApiResponse(posts)
        elif post_id == 'new':
            form = PostForm()
            return ApiResponse(form)
        else:
            post = get_object_or_404(Post, pk=post_id, author=request.user)
            return ApiResponse(post)

    def post(self, request, post_id):
        post = request.POST

        if post_id == 'new':
            instance = Post()
            instance.author = request.user
        elif post_id == 'publish':
            post = json.loads(request.body.decode())
            instance = get_object_or_404(Post, pk=post['id'], author=request.user)
        else:
            instance = get_object_or_404(Post, pk=post_id, author=request.user)

        if post_id == 'publish':
            form = PostPublishForm(post, instance=instance)
        else:
            form = PostForm(post, request.FILES, instance=instance)

        if form.is_valid():
            form.save()
            return ApiResponse(form)
        else:
            return ApiResponse(form.errors, status_code=status.HTTP_400_BAD_REQUEST)
