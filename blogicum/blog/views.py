from datetime import datetime

from blog.models import Category, Post
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, UpdateView

COUNT_POSTS = 10

User = get_user_model()


def get_posts(post_objects=Post.objects):
    return post_objects.select_related(
        'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    ).order_by('-pub_date')


def index(request):
    template = 'blog/index.html'
    post_list = get_posts().annotate(comment_count=Count('comments'))
    paginator = Paginator(post_list, COUNT_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        get_posts(),
        pk=id
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    post_list = get_posts(category.posts)
    page_number = request.GET.get('page')
    paginator = Paginator(post_list, COUNT_POSTS)
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        "page_obj": page_obj
    }
    return render(request, template, context)


class ProfileListView(ListView):
    model = Post
    paginate_by = COUNT_POSTS
    template_name = 'blog/profile.html'

    def get_user(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username']
        )

    def get_queryset(self):
        author = self.get_user()
        if author == self.request.user:
            return author.posts
        return get_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_user()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            "blog:profile",
            kwargs={"username": self.request.user.username}
        )
