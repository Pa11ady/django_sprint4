from django.urls import path

from . import views

app_name = 'blog'


def test():
    pass


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    path('profile/<slug:username>/', test,
         name='profile'),
    path('profile/<slug:username>/edit/', test,
         name='edit_profile'),
]
