from django.urls import re_path, path
from . import views

app_name = "images"

urlpatterns = [
    path('', views.Feed.as_view(), name='feed'),
    path('<int:image_id>/like/', views.LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/unlike/', views.UnlikeImage.as_view(), name='unlike_image'),
    path('<int:image_id>/comment/', views.CommentOnImage.as_view(), name='comment_on_image'),
    path('comment/<int:comment_id>/', views.Comment.as_view(),name='comment'),
    path('search/', views.Search.as_view(), name='search'),

]
