# coding: utf-8

from django.core.urlresolvers import reverse
from django.shortcuts import render

from ..admin.forms import PostForm


def index(request, **kwargs):
    new_post_url = reverse('edit', urlconf='bangoo.plugins.blog.admin.urls', args=['new'], prefix='')
    return render(request, 'blog/admin/index.html', {'new_post_url': new_post_url})

def post(request, id):
    return render(request, 'blog/admin/edit.html', {'post_id': id, 'form': PostForm()})
