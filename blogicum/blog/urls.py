from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/create/', views.create_post, name='create_post'),
    path('registration/', views.registration, name='registration'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),

    path('posts/<int:post_id>/comment/',
         views.add_comment,
         name='add_comment'
         ),

    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.delete_comment, name='delete_comment'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile_redirect/', views.profile_redirect, name='profile_redirect'),
]
