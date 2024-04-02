from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Count

from .constants import PER_PAGE
from .models import Post


def get_posts(post_objects=Post.objects):
    return post_objects.select_related(
        'category', 'location', 'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    ).order_by('-pub_date').annotate(comment_count=Count('comments'))


def get_page_obj(object_list, page_number):
    return Paginator(object_list, PER_PAGE).get_page(page_number)
