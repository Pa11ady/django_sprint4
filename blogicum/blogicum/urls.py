from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
]


handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.server_error'
