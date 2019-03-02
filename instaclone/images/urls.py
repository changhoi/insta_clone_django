from django.urls import re_path, path
from . import views

app_name = "images"

urlpatterns = [
    re_path(r'^all/$', views.ListAllImages.as_view(), name='all_images'),
    path('comments/', views.ListAllComments.as_view(), name='all_comments'),
    path('likes/', views.ListAllLikes.as_view(), name='all_likes'),
]
