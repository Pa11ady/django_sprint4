from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'blog'


def test():
    pass


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<slug:username>/', views.ProfileListView.as_view(),
         name='profile'),
    path('profile/<slug:username>/edit/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
