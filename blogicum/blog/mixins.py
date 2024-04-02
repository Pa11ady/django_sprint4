from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from .forms import PostForm
from .models import Comment, Post


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class AuthorizationMixin(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(
            Post,
            pk=kwargs['pk']
        )
        if (request.user != post.author):
            return redirect('blog:post_detail', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)


class CommentMixin(LoginRequiredMixin, View):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(
            Comment,
            pk=kwargs['pk']
        )
        if comment.author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']})
