from django.shortcuts import render
from ..models import Post
from bangoo.decorators import class_view_decorator
from django.contrib.auth.decorators import permission_required
from ajaxtables.views import AjaxListView
from blog.admin.forms import EditPostForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


@class_view_decorator(permission_required('blog.list_post'))
class PostList(AjaxListView):
    model = Post
    template_names = ['blog/admin/list.html', 'blog/admin/list_data.html']

    def get_queryset(self):
        return self.model.objects.language('hu').all().order_by('-created')


@permission_required('bangoo.add_post')
def edit_blog_post(request, post_id, template_name='blog/admin/edit_post.html'):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        post = Post()
    form = EditPostForm(request.POST or None, instance=post, initial={'authors': [request.user]})
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('blog-admin-post-list'))
    return render(request, template_name, {'form': form})