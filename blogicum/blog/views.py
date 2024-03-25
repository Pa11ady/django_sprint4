from django.shortcuts import get_object_or_404, render
from datetime import datetime

from blog.models import Category, Post


COUNT_POSTS = 5


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
    post_list = get_posts()[0:COUNT_POSTS]
    context = {
        'post_list': post_list
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
    context = {
        'category': category,
        'post_list': get_posts(category.posts)
    }
    return render(request, template, context)
