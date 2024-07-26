"""
URL configuration for SocialNetwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from network.views import *
from user.views import *

# from user import views

# Для media
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    
    path('create-post/', create_post, name='create_post'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),

    path('post/<int:post_id>/add_comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

    path('toggle_like/<int:post_id>/', toggle_like, name='toggle_like'),

    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('edit_profile/', edit_profile, name='edit_profile'),

    path('chats/', chat_list_view, name='chat_list'),
    path('chats/create/', create_chat_view, name='create_chat'),
    path('chats/delete/<int:chat_id>/', delete_chat_view, name='delete_chat'),
    
    path('chats/<int:chat_id>/', chat_detail_view, name='chat_detail'),
    path('chats/<int:chat_id>/send/', send_message_view, name='send_message'),
    path('messages/<int:message_id>/edit/', edit_message_view, name='edit_message'),
    path('messages/<int:message_id>/delete/', delete_message_view, name='delete_message'),

    path('friends/', friends_list_view, name='friends_list'),
    path('friend_requests/', friend_requests_view, name='friend_requests'),

    path('users/<int:user_id>/send_friend_request/', send_friend_request, name='send_friend_request'),
    path('cancel_friend_request/<int:request_id>/', cancel_friend_request, name='cancel_friend_request'),

    path('accept_friend_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('unfriend/<int:user_id>/', unfriend, name='unfriend'),
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
