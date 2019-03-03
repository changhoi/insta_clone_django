from django.urls import path


from instaclone.users import views

app_name = "users"
urlpatterns = [
    path("explore/", view=views.ExploreUsers.as_view(), name="explore"),
    path("search/", views.Search.as_view(), name='search'),
    path("<int:user_id>/follow", views.FollowUser.as_view(), name='follow_user'),
    path("<int:user_id>/unfollow", views.UnfollowUser.as_view(), name='unfollow_user'),
    path("<str:username>/", views.UserProfile.as_view(), name='user_profile'),
    path("<str:username>/followers/", views.UserFollowers.as_view(), name='user_followers'),
    path("<str:username>/following/", views.UserFollowing.as_view(), name='user_followers'),
]
