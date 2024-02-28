from django.urls import path

from . import views as posts_views

app_name = 'posts'

urlpatterns = [
    path('',
         posts_views.index,
         name='index'),

    path('group/<slug:slug>/',
         posts_views.group_list,
         name='group_list'),

    path('profile/<str:username>/',
         posts_views.profile,
         name='profile'),

    path('posts/<int:post_id>/',
         posts_views.post_detail,
         name='post_detail'),

    path('create/',
         posts_views.post_create,
         name='post_create'),

    path('posts/<int:post_id>/edit/',
         posts_views.post_edit,
         name='post_edit'),

    path('posts/<int:post_id>/comment/',
         posts_views.add_comment,
         name='add_comment'),

    path('follow/',
         posts_views.follow_index,
         name='follow_index'),

    path('profile/<str:username>/follow/',
         posts_views.profile_follow,
         name='profile_follow'),

    path('profile/<str:username>/unfollow/',
         posts_views.profile_unfollow,
         name='profile_unfollow'),
]
